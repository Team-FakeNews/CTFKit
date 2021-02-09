from constructs import Construct
from cdktf import Resource, TerraformOutput
from cdktf_cdktf_provider_google import ContainerCluster

from ctfkit.models.ctf_config import ClusterConfig
from ctfkit.models import CtfConfig, DeploymentConfig


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
            cluster_config: ClusterConfig) -> None:
        super().__init__(scope, name)

        self.cluster = ContainerCluster(
            self,
            'gke',
            name="ctf-cluster",
            initial_node_count=cluster_config.node_count
        )

    @property
    def username(self):
        """
        Terraform output: Username to use to connect to the kubernetes endpoint
        """
        return TerraformOutput(
            self,
            'username',
            sensitive=True,
            value=self.cluster.master_auth[0].username
        )

    @property
    def password(self):
        """
        Terraform output: Password to use to connect to the kubernetes endpoint
        """
        return TerraformOutput(
            self,
            'password',
            sensitive=True,
            value=self.cluster.master_auth[0].password
        )

    @property
    def endpoint(self):
        """
        Terraform output: Endpoint of the kubernetes API
        """
        return TerraformOutput(
            self,
            'endpoint',
            value=self.cluster.endpoint
        )
