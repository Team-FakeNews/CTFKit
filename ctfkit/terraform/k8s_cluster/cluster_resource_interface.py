from abc import ABC, abstractproperty

class K8sClusterResource(ABC):
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
        """
        Client key to use to connect to the kubernetes cluster
        """

    @abstractproperty
    def client_certificate(self) -> str:
        """
        Client certificate to use to connect to the kubernetes cluster
        """
