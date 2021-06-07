from constructs import Construct
from cdktf import Resource, TerraformOutput
from cdktf_cdktf_provider_google import ContainerCluster, ContainerClusterMasterAuth, ContainerClusterMasterAuthClientCertificateConfig

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

    @property
    def endpoint(self) -> str:
        return self.cluster.endpoint

    @property
    def username(self) -> str:
        return f'${{{self.cluster.id[2:-4]}.master_auth.0.username}}'

    @property
    def password(self) -> str:
        return f'${{{self.cluster.id[2:-4]}.master_auth.0.password}}'

    # @property
    # def cluster_ca_certificate(self) -> str:
    #     return self.cluster.master_auth[0].

    # @property
    # def client_key(self) -> str:
    #     return self.cluster.kube_config('0').client_key

    # @property
    # def client_certificate(self) -> str:
    #     return self.cluster.kube_config('0').client_certificate