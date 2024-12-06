import pulumi

from common.config.config import KubernetesConfig
from common.constants import KUBERNETES_MASTER_TYPE, KUBERNETES_NODE_TYPE
from common.servers.base import PrivateServer


class Cluster(pulumi.ComponentResource):
    servers: list[PrivateServer] = []
    master: list[PrivateServer] = []
    nodes: list[PrivateServer] = []

    def __init__(
        self,
        type: str,
        config: KubernetesConfig,
        opts=None,
    ):
        super().__init__(f"sys-int:cluster:{type}", f"cluster-{type.lower()}-{config.cluster_name}", None, opts)
        """Create a new cluster."""
        for i in range(config.master_nodes):
            node_name = f"{config.cluster_name}-master-{i}"
            server_type = KUBERNETES_MASTER_TYPE
            server = PrivateServer(
                node_name,
                config.current_network,
                config.firewall,
                config.ssh_keys,
                {
                    "server_type": server_type,
                },
                opts=pulumi.ResourceOptions(parent=self),
            )
            self.master.append(server)
        for i in range(config.node_count):
            node_name = f"{config.cluster_name}-node-{i}"
            server_type = KUBERNETES_NODE_TYPE
            server = PrivateServer(
                node_name,
                config.current_network,
                config.firewall,
                config.ssh_keys,
                {
                    "server_type": server_type,
                },
                opts=pulumi.ResourceOptions(parent=self),
            )
            self.master.append(server)
        pass
