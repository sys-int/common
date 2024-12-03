import pulumi
from icecream import ic
from pulumi_hcloud import Network, Server


class PrivateServer(pulumi.ComponentResource):
    def __init__(self, name, network: Network, server_args, opts=None):
        network_name = network.name
        network_id = network.id
        super().__init__(
            "sys-int:servers:PrivateServer",
            f"{network_name}-{name}",
            None,
            opts,
        )
        ic(network_id)

        # Create the server with private network interface
        server = Server(
            f"{network_name}-{name}-server",
            name=name,
            server_type=server_args["server_type"],
            image="ubuntu-24.04",
            public_nets=[
                {
                    "ipv4_enabled": False,
                    "ipv6_enabled": False,
                }
            ],
            networks=[
                {
                    "network_id": network_id,
                }
            ],
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.server = server
        self.private_network = network

        self.register_outputs(
            {
                "server": self.server,
                "private_network": self.private_network,
            }
        )
