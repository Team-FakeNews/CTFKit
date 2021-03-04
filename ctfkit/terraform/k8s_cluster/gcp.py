from constructs import Construct
from cdktf import Resource, TerraformOutput
from cdktf_cdktf_provider_google import ContainerCluster

from ctfkit.models.ctf_config import GcpConfig


class GcpGKE(Resource):
    """
    Manage a Google Kubernetes Engine to build up our cluster
    Some settings can be managed by the user through the provided configuration
    """

    cluster: ContainerCluster

    def __init__(
            self,
            scope: Construct,
            name: str,
            gcp_config: GcpConfig) -> None:
        super().__init__(scope, name)

        self.cluster = ContainerCluster(
            self,
            'gke',
            name="ctf-cluster",
            initial_node_count=gcp_config.node_count
        )

        # self.client_certificate = TerraformOutput(
        #     self,
        #     'username',
        #     sensitive=True,
        #     value=self.cluster.master_auth.pop().client_certificate
        # )
