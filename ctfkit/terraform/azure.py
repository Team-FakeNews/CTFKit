from constructs import Construct
from cdktf import Resource, TerraformOutput
from cdktf_cdktf_provider_azurerm import KubernetesCluster, KubernetesClusterAddonProfile, KubernetesClusterAddonProfileKubeDashboard, KubernetesClusterDefaultNodePool, KubernetesClusterNetworkProfile, ResourceGroup

from ctfkit.models.ctf_config import AzureConfig
from .cluster_resource import ClusterResource

class AzureAKS(Resource, ClusterResource):
    """
    Manage an Azure Kubernetes Service to build up our cluster
    Some settings can be managed by the user through the provided configuration
    """

    cluster: KubernetesCluster

    def __init__(
            self,
            scope: Construct,
            name: str,
            azure_config: AzureConfig) -> None:
        super().__init__(scope, name)

        resource_group = ResourceGroup(
            self,
            'resource_group',
            name=name,
            location=azure_config.location
        )

        self.cluster = KubernetesCluster(
            self,
            'aks',

            name="ctf-cluster",
            location=azure_config.location,
            resource_group_name=resource_group.name,
            dns_prefix='ctf',
            default_node_pool=[KubernetesClusterDefaultNodePool(
                name='default',
                node_count=azure_config.node_count,
                vm_size=azure_config.vm_size,
                enable_auto_scaling=True
            )],

            network_profile=[KubernetesClusterNetworkProfile(
                network_plugin="kubenet",
                load_balancer_sku="Standard"
            )],

            addon_profile=[KubernetesClusterAddonProfile(
                kube_dashboard=[KubernetesClusterAddonProfileKubeDashboard(enabled=True)]
            )]
        )

    @property
    def cluster_ca_certificate(self) -> TerraformOutput:
        return self.cluster.kube_config.cluster_ca_certificate
