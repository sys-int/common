import pulumi
from pulumi import Output, StackReference
from pulumi_hcloud import AwaitableGetNetworkResult, Server, ServerNetworkArgs

import common
from common.constants import SERVER_IMAGE


def get_ssh_keys():
    base_stack = StackReference("private-server-ssh-stack", "eBeyond/base/main")
    return base_stack.get_output("ssh_keys")


class PrivateServer(pulumi.ComponentResource):
    def __init__(
        self,
        name,
        network: AwaitableGetNetworkResult,
        firewall: Output[str],
        ssh_keys,
        server_type: str = "cx22",
        opts=None,
    ):
        super().__init__("sys-int:servers:PrivateServer", f"server-private-{name}", None, opts)
        network_name = network.name
        arg = ServerNetworkArgs(network_id=network.id)

        # Create the server with private network interface
        server = Server(
            f"{network_name}-{name}-server",
            name=name,
            server_type=server_type,
            image=SERVER_IMAGE,
            public_nets=[
                {
                    "ipv4_enabled": False,
                    "ipv6_enabled": False,
                }
            ],
            networks=[arg],
            user_data=common.servers.user_data.create_user_data(
                network=network, firewall=firewall, private_networking=True
            ),
            ssh_keys=ssh_keys,
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
