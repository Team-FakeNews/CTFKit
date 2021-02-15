from abc import ABC, abstractproperty
from cdktf import TerraformOutput

class ClusterResource(ABC):
    """
    A class which implement ClusterResource is a Terraform Ressource
    which managed a kubernetes cluster. It can be a self-managed cluster or a cluster
    provided by a cloud provider
    """

    @abstractproperty
    def cluster_ca_certificate(self) -> TerraformOutput:
        """
        Cluster CA certificate to use to connect to the kubernetes cluster
        """

    # @abstractproperty
    # def client_certificate(self) -> TerraformOutput:
    #     """
    #     Client certificate to use to connect to the kubernetes cluster
    #     """
