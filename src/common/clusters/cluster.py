import pulumi
from pulumi_hcloud import Network

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
        firewall_ip: str,
        server_type: str = "cx11",
        opts=None,
    ):
        super().__init__(f"sys-int:cluster:{type}", f"cluster-{type.lower()}-{name}", None, opts)
        """Create a new cluster."""
        for i in range(node_count):
            if i < master_nodes:
                node_name = f"{name}-master-{i}"
            else:
                node_name = f"{name}-node-{i}"
            server = PrivateServer(
                node_name,
                cluster_network,
                firewall_ip,
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
