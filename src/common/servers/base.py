import pulumi
from icecream import ic
from pulumi_hcloud import Network, Server, ServerNetworkArgs

import common.servers.user_data


class PrivateServer(pulumi.ComponentResource):
    def __init__(self, name, network: Network, firewall_ip: str, server_args, opts=None):
        super().__init__("sys-int:servers:PrivateServer", f"server-private-{name}", None, opts)
        network_name = network.name
        network_id: int = int(network.id)
        ic(network_id)
        arg = ServerNetworkArgs(network_id=network_id)

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
            networks=[arg],
            user_data=common.servers.user_data.create_user_data(
                network=network, firewall_ip=firewall_ip, private_networking=True
            ),
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.server = server
        self.private_network = network

        self.register_outputs(
            {
                "server": self.server.id,
                "private_network": self.private_network.id,
            }
        )
