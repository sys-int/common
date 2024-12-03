import pulumi
from pulumi_hcloud import Network, Server


class PrivateServer(pulumi.ComponentResource):
    def __init__(self, name, private_network: Network, server_args, opts=None):
        network_name = private_network.name
        super().__init__(
            "sys-int:servers:PrivateServer",
            f"{network_name}-{name}",
            None,
            opts,
        )

        # Create the server with private network interface
        server = Server(
            f"{network_name}-{name}-server",
            name=name,
            server_type=server_args["server_type"],
            image=server_args["image"],
            public_nets=[
                {
                    "ipv4_enabled": False,
                    "ipv6_enabled": False,
                }
            ],
            networks=[{"network_id": str(private_network.id)}],
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.server = server
        self.private_network = private_network

        self.register_outputs(
            {
                "server": self.server,
                "private_network": self.private_network,
            }
        )
