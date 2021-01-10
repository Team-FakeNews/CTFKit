from constructs import Construct
from cdktf import Resource
from cdktf_cdktf_provider_google import ContainerCluster

from ctfkit.models import CtfConfig, DeploymentConfig


class GcpK8sCluster(Resource):

    def __init__(self, scope: Construct, id: str, config: CtfConfig, deployment: DeploymentConfig) -> None:
        super().__init__(scope, id)

        ContainerCluster(
            self,
            'k8s_cluster',
            name=f"ctf-cluster-{config.getSlug()}",
            initial_node_count=deployment.cluster.node_count
        )
