import logging
import os
import random
import time

from faas.system import Clock, LoggingLogger
from kubernetes import config, client
from telemc import TelemetryController

from examples.basic.podfactory import BasicExamplePodFactory
from galileofaas.connections import RedisClient
from galileofaas.context.daemon import GalileoFaasContextDaemon
from galileofaas.context.model import GalileoFaasContext
from galileofaas.context.platform.deployment.factory import create_deployment_service
from galileofaas.context.platform.network.factory import create_network_service
from galileofaas.context.platform.node.factory import create_node_service
from galileofaas.context.platform.replica.factory import create_replica_service, KubernetesFunctionReplicaFactory
from galileofaas.context.platform.telemetry.factory import create_telemetry_service
from galileofaas.context.platform.trace.factory import create_trace_service
from galileofaas.context.platform.zone.factory import create_zone_service
from galileofaas.system.core import GalileoFaasMetrics
from galileofaas.system.faas import GalileoFaasSystem
from galileofaas.system.metrics import GalileoLogger

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging._nameToLevel[os.environ.get('galileo_faas_logging', 'DEBUG')])
    rds = RedisClient.from_env()
    metrics = setup_metrics()
    daemon = setup_daemon(rds, metrics)

    faas_system = GalileoFaasSystem(daemon.context, metrics)

    # start the subscribers to listen for telemetry, traces and Pods
    daemon.start()
    time.sleep(3)
    nodes = daemon.context.node_service.get_nodes()
    logger.info(f'Available nodes: {[n.name for n in nodes]}')
    cpu = daemon.context.telemetry_service.get_node_resource(nodes[0].name, 'cpu')
    logger.info(f'Mean CPU usage of node {nodes[0].name}: {cpu["value"].mean()}')
    # shut down
    daemon.stop(timeout=5)
    rds.close()


def setup_metrics(clock: Clock = None, rds: RedisClient = None):
    if rds is not None:
        metric_logger = GalileoLogger(rds, clock)
    else:
        log_fn = lambda x: logger.info(f'[log] {x}')
        metric_logger = LoggingLogger(log_fn, clock)
    return GalileoFaasMetrics(metric_logger)


def setup_daemon(rds: RedisClient, metrics: GalileoFaasMetrics) -> GalileoFaasContextDaemon:
    deployment_service = create_deployment_service(metrics)

    telemc = TelemetryController(rds.conn())
    node_service = create_node_service(telemc)

    # latency in ms
    min_latency = 1
    max_latency = 1000
    latency_map = {}
    nodes = node_service.get_nodes()
    for node_1 in nodes:
        for node_2 in nodes:
            if node_1 == node_2:
                # same node has 0.5 ms latency
                latency_map[(node_1.name, node_2.name)] = 0.5
            else:
                # else make random for demonstration purposes
                # TODO this has to be updated for the specific testbed (or use Ether to model the topology)
                latency_map[(node_1.name, node_2.name)] = random.randint(1, 100)
    network_service = create_network_service(min_latency, max_latency, latency_map)

    pod_factory = BasicExamplePodFactory()
    config.load_kube_config()
    core_v1_api = client.CoreV1Api()
    replica_factory = KubernetesFunctionReplicaFactory()
    replica_service = create_replica_service(node_service, rds, deployment_service, core_v1_api, pod_factory,
                                             replica_factory, metrics)

    # window size to store, in seconds
    window_size = 3 * 60
    telemetry_service = create_telemetry_service(window_size, rds, node_service)

    trace_service = create_trace_service(window_size, rds, replica_service, network_service, node_service)

    zones = node_service.get_zones()
    zone_service = create_zone_service(zones)

    context = GalileoFaasContext(
        deployment_service,
        network_service,
        node_service,
        replica_service,
        telemetry_service,
        trace_service,
        zone_service,
        KubernetesFunctionReplicaFactory(),
        rds,
        telemc
    )
    return GalileoFaasContextDaemon(context)


if __name__ == '__main__':
    main()
