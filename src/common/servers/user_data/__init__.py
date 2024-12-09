from abc import ABC, abstractmethod

from pulumi import Output
from pulumi_hcloud import GetNetworkResult


def create_user_data(network: GetNetworkResult, firewall: Output[str], private_networking: bool = False) -> Output[str]:
    firewall_ip = Output.all(firewall=firewall, network=network).apply(
        lambda x: x["firewall"]["privateIPs"][x["network"].name]
    )
    dns_ip = Output.all(firewall=firewall, network=network).apply(
        lambda x: x["firewall"]["privateIPs"][x["network"].name]
    )
    gateway_ip = Output.all(firewall=firewall, network=network).apply(
        lambda x: x["firewall"]["privateIPs"][x["network"].name][
            : x["firewall"]["privateIPs"][x["network"].name].rfind(".") + 1
        ]
        + "1"
    )
    network_ip = Output.all(firewall=firewall, network=network).apply(
        lambda x: x["firewall"]["privateIPs"][x["network"].name][
            : x["firewall"]["privateIPs"][x["network"].name].rfind(".") + 1
        ]
        + "0/24"
    )

    result = Output.all(firewall_ip=firewall_ip, dns_ip=dns_ip, gateway_ip=gateway_ip, network=network_ip).apply(
        lambda x: f"""
#cloud-config
runcmd:
    - sed -ie '/^PermitRootLogin/s/^.*$/PermitRootLogin yes/' /etc/ssh/sshd_config
    - sed -ie '/^PasswordAuthentication/s/^.*$/PasswordAuthentication yes/' /etc/ssh/sshd_config
    - sed -ie '/^X11Forwarding/s/^.*$/X11Forwarding yes/' /etc/ssh/sshd_config
    - sed -ie '/^#MaxAuthTries/s/^.*$/MaxAuthTries 3/' /etc/ssh/sshd_config
    - sed -ie '/^#AllowTcpForwarding/s/^.*$/AllowTcpForwarding yes/' /etc/ssh/sshd_config
    - sed -ie '/^#AllowAgentForwarding/s/^.*$/AllowAgentForwarding yes/' /etc/ssh/sshd_config
    - systemctl restart ssh
    - export IFACE=$(ip -br l | awk '$1 !~ "lo|vir|wl|ve|br|do" {{ print $1}}')
    - sed -ie 's/IFACE/'"$IFACE"'/g' /etc/netplan/netplan.yaml
    - export IPADDRESS=$(ip -br a | awk '$1 == "'"$IFACE"'" {{ print $3}}' | cut -d/ -f1)
    - sed -ie 's/IPADDRESS/'"$IPADDRESS"'/g' /etc/netplan/netplan.yaml
    - netplan apply
write_files:
    - content: |
        network: {{config: disabled}}
      permissions: '0644'
      path: /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
    - content: |
network:
    version: 2
    renderer: networkd
    ethernets:
        IFACE:
            addresses:
                - IPADDRESS
                mtu: 1450
            routes:
                - to: {x["network"]}
                  via: {x["gateway_ip"]}
                  on-link: true
                - to: {x["gateway_ip"]}
                  via: 0.0.0.0
                - to: 0.0.0.0/0
                  via: {x["gateway_ip"]}
                  on-link: true
                - to: 169.254.169.254/32
                  via: {x["gateway_ip"]}
                  on-link: true
            nameservers:
                addresses:
                    - {x["dns_ip"]}
      path: /etc/netplan/netplan.yaml
      permissions: '0644'
    """
    )
    return result


class WriteFile:
    def __init__(self, content: str, permissions: str, path: str):
        self.content = content
        self.permissions = permissions
        self.path = path
        pass

    pass


class UserData(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def getRunCmds(self) -> list[str]:
        pass

    #
    # @abstractmethod
    # def getWriteFiles(self) -> WriteFile[]:
    #     pass
