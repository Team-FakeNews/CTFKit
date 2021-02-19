from abc import ABC, abstractproperty
from cdktf import TerraformOutput

class ClusterResource(ABC):
    """
    A class which implement ClusterResource is a Terraform Ressource
    which managed a kubernetes cluster. It can be a self-managed cluster or a cluster
    provided by a cloud provider
    """

    @abstractproperty
    def cluster_ca_certificate(self) -> str:
        """
        Cluster CA certificate to use to connect to the kubernetes cluster
        """

    @abstractproperty
    def client_key(self) -> str:
        pass
        # return self.cluster.kube_config('0').client_key

    @abstractproperty
    def client_certificate(self) -> str:
        pass
        # return self.cluster.kube_config('0').client_certificate
