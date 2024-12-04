from pulumi_hcloud import Network

from common.clusters.kubernetes import KubernetesCluster


def createKubernetesCluster(name: str, node_count: int, master_nodes: int, cluster_network: Network, firewall_ip: str):
    """Create a new cluster."""
    cluster = KubernetesCluster(
        name=name,
        node_count=node_count,
        master_nodes=master_nodes,
        cluster_network=cluster_network,
        firewall_ip=firewall_ip,
        server_type="cx11",
    )
    return cluster
