from constructs import Construct
from cdktf import Resource
from cdktf_cdktf_provider_azurerm import KubernetesCluster, KubernetesClusterAddonProfile, KubernetesClusterDefaultNodePool, KubernetesClusterNetworkProfile, ResourceGroup

from ctfkit.models.ctf_config import ClusterConfig
from ctfkit.models import CtfConfig, DeploymentConfig


class AzureAKS(Resource):
    """
    Manage an Azure Kubernetes Service to build up our cluster
    Some settings can be managed by the user through the provided configuration
    """

    def __init__(
            self,
            scope: Construct,
            name: str,
            cluster_config: ClusterConfig) -> None:
        super().__init__(scope, name)

        resource_group = ResourceGroup(
            self,
            name=self.name,
            location=cluster_config.location
        )

        KubernetesCluster(
            self,
            'aks',
            location=cluster_config.location,
            resource_group_name=resource_group.name,
            dns_prefix='ctf-',
            
            default_node_pool=KubernetesClusterDefaultNodePool(
                name='default',
                node_count=cluster_config.node_count,
                vm_size=cluster_config.machine_type,
                enable_auto_scaling=True
            ),

            network_profile=KubernetesClusterNetworkProfile(
                network_plugin="kubenet",
                load_balancer_sku="Standard"
            ),

            addon_profile=KubernetesClusterAddonProfile(
                kube_dashboard=True
            )
        )
