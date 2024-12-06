import pulumi
from pulumi import Output
from pulumi_hcloud import Network

from common.constants import KUBERNETES_MASTER_TYPE, KUBERNETES_NODE_TYPE
from common.servers.base import PrivateServer


class Cluster(pulumi.ComponentResource):
    servers: list[PrivateServer] = []
    master: list[PrivateServer] = []
    nodes: list[PrivateServer] = []

    def __init__(
        self,
        type: str,
        name: str,
        node_count: int,
        master_nodes: int,
        cluster_network: Network,
        firewall: Output[str],
        opts=None,
    ):
        super().__init__(f"sys-int:cluster:{type}", f"cluster-{type.lower()}-{name}", None, opts)
        """Create a new cluster."""
        for i in range(node_count):
            if i < master_nodes:
                node_name = f"{name}-master-{i}"
                server_type = KUBERNETES_MASTER_TYPE
            else:
                node_name = f"{name}-node-{i}"
                server_type = KUBERNETES_NODE_TYPE
            server = PrivateServer(
                node_name,
                cluster_network,
                firewall,
                {
                    "server_type": server_type,
                },
                opts=pulumi.ResourceOptions(parent=self),
            )
            self.servers.append(server)
            if i < master_nodes:
                self.master.append(server)
            else:
                self.nodes.append(server)
            pass
        pass
