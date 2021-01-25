from ctfkit.models.ctf_config import ClusterConfig
from constructs import Construct
from cdktf import Resource
from cdktf_cdktf_provider_google import ContainerCluster

from ctfkit.models import CtfConfig, DeploymentConfig


class GcpGKE(Resource):
    """
    Manage a Google Kubernetes Engine to build up our cluster
    Some settings can be managed by the user through the provided configuration
    """

    def __init__(
            self,
            scope: Construct,
            name: str,
            cluster_config: ClusterConfig) -> None:
        super().__init__(scope, name)

        ContainerCluster(
            self,
            'gke',
            name=f"ctf-cluster",
            initial_node_count=cluster_config.node_count
        )
