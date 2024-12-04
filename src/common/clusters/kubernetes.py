import pulumi
from pulumi_hcloud import Network

from common.servers.base import PrivateServer


class KubernetesCluster(pulumi.ComponentResource):
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
        super().__init__("sys-int:cluster:Kubernetes", f"cluster-kubernetes-{name}", None, opts)
        """Create a new cluster."""
        for i in range(node_count):
            server = PrivateServer(
                f"{name}-node-{i}",
                cluster_network,
                {
                    "server_type": server_type,
                },
            )
            self.servers.append(server)
            if i < master_nodes:
                self.master.append(server)
            else:
                self.nodes.append(server)
            pass
        pass
