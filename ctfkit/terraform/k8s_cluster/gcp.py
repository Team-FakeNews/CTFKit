from constructs import Construct
from cdktf import Resource, TerraformOutput
from cdktf_cdktf_provider_google import ContainerCluster, ContainerClusterMasterAuth, ContainerClusterMasterAuthClientCertificateConfig, ContainerClusterNodeConfig, ContainerClusterNodePool, ContainerClusterNodePoolAutoscaling, ContainerClusterPrivateClusterConfig, ContainerNodePool, ContainerNodePoolAutoscaling, ContainerNodePoolNodeConfig, DataGoogleClientConfig, ServiceAccount

from ctfkit.models.ctf_config import GcpConfig


class GcpGKE(Resource):
    """
    Manage a Google Kubernetes Engine to build up our cluster
    Some settings can be managed by the user through the provided configuration
    """

    cluster: ContainerCluster
    node_pool: ContainerNodePool

    def __init__(
            self,
            scope: Construct,
            name: str,
            gcp_config: GcpConfig) -> None:
        super().__init__(scope, name)
        print("INIT")

        sa = ServiceAccount(
            self,
            'k8s_sa',
            account_id='ctf-cluster-sa',
            display_name='Ctf Cluter'
        )

        self.cluster = ContainerCluster(
            self,
            'gke',
            name="ctf-cluster",
            # initial_node_count=gcp_config.node_count,
            initial_node_count=1,
            # private_cluster_config=[ContainerClusterPrivateClusterConfig(
            #     enable_private_nodes=True,
            #     enable_private_endpoint=False
            # )]
        )

        self.node_pool = ContainerNodePool(
            self.cluster,
            'challenges_node_pool',
            name='challenges-node-pool',
            cluster=self.cluster.name,
            initial_node_count=1,
            autoscaling=[ContainerNodePoolAutoscaling(
                min_node_count=1,
                max_node_count=10
            )],
            node_config=[ContainerNodePoolNodeConfig(
                preemptible=True,
                machine_type=gcp_config.machine_type,
                service_account=sa.email,
                oauth_scopes = [
                    'https://www.googleapis.com/auth/cloud-platform'
                ]
            )]
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
