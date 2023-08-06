import json
import logging
import threading
from typing import Dict, List, Optional, Callable, Union

from faas.context import InMemoryFunctionReplicaService, FunctionReplicaService, NodeService, FunctionDeploymentService
from faas.system import FunctionReplicaState
from faas.system.exception import FunctionReplicaCreationException
from faas.util.constant import hostname_label, zone_label
from kubernetes import client
from kubernetes.client import ApiException

from galileofaas.connections import RedisClient
from galileofaas.context.platform.pod.factory import PodFactory
from galileofaas.context.platform.replica.model import parse_function_replica
from galileofaas.system.core import KubernetesFunctionReplica, KubernetesFunctionNode, KubernetesFunctionDeployment, \
    GalileoFaasMetrics
from galileofaas.system.k8s.create import create_pod_from_replica
from galileofaas.system.k8s.delete import delete_pod
from galileofaas.util.pubsub import POISON

logger = logging.getLogger(__name__)


class KubernetesFunctionReplicaService(FunctionReplicaService[KubernetesFunctionReplica]):
    """
    This implementation of the FunctionReplicaService uses internally a InMemoryFunctionReplicaService
    that manages the in-memory state.
    Further, it modifies the connected Kubernetes cluster (i.e., add_function_replica will create a corresponding Pod
    in the cluster).
    It does however keep, as mentioned already, an in-memory state - which means that Kubernetes is never invoked
    to retrieve any pods.
    This implementation offers the ability to run as daemon and listen for events published via Redis.
    Specifically listens on events emitted from the telemd-kubernetes-adapter.
    """

    def __init__(self, replica_service: InMemoryFunctionReplicaService[KubernetesFunctionReplica],
                 rds_client: RedisClient,
                 node_service: NodeService[KubernetesFunctionNode],
                 deployment_service: FunctionDeploymentService[KubernetesFunctionDeployment],
                 core_v1_api: client.CoreV1Api,
                 pod_factory: PodFactory,
                 async_pod: bool,
                 metrics: GalileoFaasMetrics,
                 channel='galileo/events'):
        super().__init__()
        self.replica_service = replica_service
        self.node_service = node_service
        self.deployment_service = deployment_service
        self.rds_client = rds_client
        self.channel = channel
        self.core_v1_api = core_v1_api
        self.pod_factory = pod_factory
        self.async_pod = async_pod
        self.metrics = metrics
        self.t = None

    def get_function_replica_with_ip(self, ip: str, running: bool = True, state: FunctionReplicaState = None) -> \
            Optional[
                KubernetesFunctionReplica]:

        def predicate(replica: KubernetesFunctionReplica) -> bool:
            return replica.ip == ip

        replicas = self.replica_service.find_by_predicate(predicate, running, state)
        if len(replicas) == 0:
            return None
        else:
            return replicas[0]

    def get_function_replicas(self) -> List[KubernetesFunctionReplica]:
        return self.replica_service.get_function_replicas()

    def get_function_replicas_of_deployment(self, fn_deployment_name, running: bool = True,
                                            state: FunctionReplicaState = None) -> List[
        KubernetesFunctionReplica]:
        return self.replica_service.get_function_replicas_of_deployment(fn_deployment_name, running, state)

    def find_function_replicas_with_labels(self, labels: Dict[str, str] = None, node_labels=None, running: bool = True,
                                           state: str = None) -> List[
        KubernetesFunctionReplica]:
        return self.replica_service.find_function_replicas_with_labels(labels, node_labels, running, state)

    def get_function_replica_by_id(self, replica_id: str) -> Optional[KubernetesFunctionReplica]:
        return self.replica_service.get_function_replica_by_id(replica_id)

    def get_function_replica_with_id(self, replica_id: str) -> Optional[KubernetesFunctionReplica]:
        return self.replica_service.get_function_replica_with_id(replica_id)

    def get_function_replicas_on_node(self, node_name: str) -> List[KubernetesFunctionReplica]:
        return self.replica_service.get_function_replicas_on_node(node_name)

    def shutdown_function_replica(self, replica_id: str):
        replica = self.replica_service.get_function_replica_by_id(replica_id)
        self.replica_service.shutdown_function_replica(replica_id)
        delete_pod(self.core_v1_api, replica_id, replica.namespace, self.async_pod)

    def delete_function_replica(self, replica_id: str):
        self.replica_service.delete_function_replica(replica_id)

    def find_by_predicate(self, predicate: Callable[[KubernetesFunctionReplica], bool], running: bool = True,
                          state: FunctionReplicaState = None) -> \
            List[KubernetesFunctionReplica]:
        return self.replica_service.find_by_predicate(predicate, running, state)

    def add_function_replica(self, replica: KubernetesFunctionReplica) -> KubernetesFunctionReplica:
        self.metrics.log_function_replica(replica)
        self.replica_service.add_function_replica(replica)
        node_selector = {}
        if replica.labels.get(zone_label, None) is not None:
            node_selector[zone_label] = replica.labels[zone_label]
        if replica.labels.get(hostname_label, None) is not None:
            node_selector[hostname_label] = replica.labels[hostname_label]

        try:
            # TODO handle async return value (i.e., error)
            create_pod_from_replica(replica, self.pod_factory, self.core_v1_api, self.async_pod,
                                    node_selector=node_selector)
            return replica
        except ApiException:
            raise FunctionReplicaCreationException()

    def scale_down(self, function_name: str, remove: Union[int, List[KubernetesFunctionReplica]]):
        removed = self.replica_service.scale_down(function_name, remove)
        for removed_replica in removed:
            self.shutdown_function_replica(removed_replica.replica_id)
        self.metrics.log_scaling(function_name, len(removed))
        return removed

    def scale_up(self, function_name: str, add: Union[int, List[KubernetesFunctionReplica]]) -> List[
        KubernetesFunctionReplica]:
        added = self.replica_service.scale_up(function_name, add)
        for added_replica in added:
            self.add_function_replica(added_replica)
        self.metrics.log_scaling(function_name, len(added))
        return added

    def run(self):
        for event in self.rds_client.sub(self.channel):
            try:
                if event['data'] == POISON:
                    break
                msg = event['data']
                logger.debug("Got message: %s", msg)
                split = msg.split(' ', maxsplit=2)
                event = split[1]
                if 'pod' in event:
                    try:
                        replica = parse_function_replica(split[2], self.deployment_service, self.node_service)
                        if replica is None:
                            logger.warning(f"Emitted pod container does not adhere to structure: {split[2]}")
                        else:
                            logger.info(f"Handler container event ({event}):  {replica.replica_id}")
                            if event == 'pod/running':
                                self.metrics.log_replica_lifecycle(replica, FunctionReplicaState.RUNNING)
                                logger.info(f"Set pod running: {replica.replica_id}")
                                self.add_function_replica(replica)
                            elif event == 'pod/delete':
                                self.metrics.log_replica_lifecycle(replica, FunctionReplicaState.DELETE)
                                logger.info(f'Delete pod {replica.replica_id}')
                                self.delete_function_replica(replica.replica_id)
                            elif event == 'pod/create':
                                logger.info(f"create pod: {replica.replica_id}")
                                self.metrics.log_replica_lifecycle(replica, FunctionReplicaState.CONCEIVED)
                                self.add_function_replica(replica)
                            elif event == 'pod/pending':
                                self.metrics.log_replica_lifecycle(replica, FunctionReplicaState.PENDING)
                                logger.info(f"pending pod: {replica.replica_id}")
                                self.add_function_replica(replica)
                            elif event == 'pod/shutdown':
                                self.metrics.log_replica_lifecycle(replica, FunctionReplicaState.SHUTDOWN)
                                logger.info(f"shutdown pod {replica.replica_id}")
                                self.shutdown_function_replica(replica.replica_id)
                            else:
                                logger.error(f'unknown pod event ({event}): {replica.replica_id}')
                    except:
                        logger.error(f"error parsing container - {msg}")
                elif event == 'scale_schedule':
                    # TODO this might need update
                    obj = json.loads(split[2])
                    if obj['delete'] is True:
                        name = obj['pod']['pod_name']
                        replica = self.get_function_replica_by_id(name)
                        logger.info(f'Got scale_schedule event. Delete replica {replica}')
                        self.shutdown_function_replica(replica.replica_id)
                else:
                    # ignore - not of interest
                    pass
            except Exception as e:
                logging.error(e)
            pass

    def start(self):
        logger.info('Start KubernetesFunctionReplicaService subscription thread')
        self.t = threading.Thread(target=self.run)
        self.t.start()
        return self.t

    def stop(self, timeout: float = 5):
        self.rds_client.close()
        if self.t is not None:
            t: threading.Thread = self.t
            t.join(timeout)
        logger.info('Stopped KubernetesFunctionReplicaService subscription thread')
