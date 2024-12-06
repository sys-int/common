from common.clusters.cluster import Cluster
from common.config.config import KubernetesConfig


class KubernetesCluster(Cluster):
    def __init__(
        self,
        config: KubernetesConfig,
        opts=None,
    ):
        super().__init__("Kubernetes", config, opts)
        pass
