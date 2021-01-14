from constructs import Construct
from cdktf import Resource
from cdktf_cdktf_provider_google import ContainerCluster

from ctfkit.models import CtfConfig, DeploymentConfig


class GcpK8sCluster(Resource):
    """
    Manage a Google Kubernetes Engine to build up our cluster
    Some settings can be managed by the user through the provided configuration
    """

    def __init__(
            self,
            scope: Construct,
            name: str,
            config: CtfConfig,
            deployment: DeploymentConfig) -> None:
        super().__init__(scope, name)

        ContainerCluster(
            self,
            'k8s_cluster',
            name=f"ctf-cluster-{config.get_slug()}",
            initial_node_count=deployment.cluster.node_count
        )