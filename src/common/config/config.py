from typing import Any

from pulumi import Output
from pulumi_hcloud import Network


class Config:
    current_network: Network
    networks: dict[str, Any]
    ssh_keys: list[str] = []
    firewall: Output[str]


class ClusterConfig(Config):
    cluster_name: str = ""
    node_count: int = 0
    master_nodes: int = 0

    def getNodeCount(self):
        return self.node_count + self.master_count


class KubernetesConfig(ClusterConfig): ...
