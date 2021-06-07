from constructs import Construct
from cdktf import Resource, TerraformOutput
from cdktf_cdktf_provider_google import ContainerCluster, ContainerClusterMasterAuth, ContainerClusterMasterAuthClientCertificateConfig, DataGoogleClientConfig

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

    @property
    def endpoint(self) -> str:
        return self.cluster.endpoint

    @property
    def cluster_ca_certificate(self) -> str:
        return f'${{{self.cluster.id[2:-4]}.master_auth.0.cluster_ca_certificate}}'

    @property
    def token(self) -> str:
        return DataGoogleClientConfig(self, 'provider').access_token

    @property
    def services_cidr(self) -> str:
        return self.cluster.services_ipv4_cidr
