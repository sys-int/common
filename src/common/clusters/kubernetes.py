from pulumi_hcloud import Network

from common.clusters.cluster import Cluster
from common.servers.base import PrivateServer


class KubernetesCluster(Cluster):
    servers: list[PrivateServer]
    master: list[PrivateServer]
    nodes: list[PrivateServer]

    def __init__(
        self,
        name,
        node_count: int,
        master_nodes: int,
        cluster_network: Network,
        firewall_ip: str,
        server_type: str = "cx11",
        opts=None,
    ):
        super().__init__("Kubernetes", name, node_count, master_nodes, cluster_network, firewall_ip, server_type, opts)
