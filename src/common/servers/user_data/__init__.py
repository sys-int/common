from abc import ABC, abstractmethod

from pulumi import Output


def create_user_data(firewall_ip: Output[str], private_networking: bool = False) -> str:
    dns_server = firewall_ip
    gateway = firewall_ip.apply(lambda x: x[: x.rfind(".") + 1] + "1")
    network = firewall_ip.apply(lambda x: x[: x.rfind(".") + 1] + "0/24")

    result = f"""
       #cloud-config
       runcmd:
            - sed -ie '/^PermitRootLogin/s/^.*$/PermitRootLogin yes/' /etc/ssh/sshd_config
            - sed -ie '/^PasswordAuthentication/s/^.*$/PasswordAuthentication no/' /etc/ssh/sshd_config
            - sed -ie '/^X11Forwarding/s/^.*$/X11Forwarding yes/' /etc/ssh/sshd_config
            - sed -ie '/^#MaxAuthTries/s/^.*$/MaxAuthTries 3/' /etc/ssh/sshd_config
            - sed -ie '/^#AllowTcpForwarding/s/^.*$/AllowTcpForwarding yes/' /etc/ssh/sshd_config
            - sed -ie '/^#AllowAgentForwarding/s/^.*$/AllowAgentForwarding yes/' /etc/ssh/sshd_config
            - systemctl restart ssh
            - export IFACE=$(ip -br l | awk '$1 !~ "lo|vir|wl|ve|br|do" {{ print $1}}'
            - sed -ie 's/IFACE/$IFACE/g' /etc/netplan/netplan.yaml
            - export IPADDRESS=$(ip -br a | awk '$1 == "$IFACE" {{ print $3}}' | cut -d/ -f1)
            - sed -ie 's/IPADDRESS/$IPADDRESS/g' /etc/netplan/netplan.yaml
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
                            - IPADDRESS/32
                        mtu: 1450
                        routes:
                            - to: {network}
                              via: {gateway}
                              on-link: true
                            - to: {gateway}
                              via: 0.0.0.0
                            - to: 0.0.0.0/0
                              via: {gateway}
                              on-link: true
                            - to: 169.254.169.254/32
                              via: {gateway}
                              on-link: true
                        nameservers:
                            addresses:
                                - {dns_server}
              path: /etc/netplan/netplan.yaml
              permissions: '0644'
    """
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
