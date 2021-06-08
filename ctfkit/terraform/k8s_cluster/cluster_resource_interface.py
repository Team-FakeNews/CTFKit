from abc import ABC, abstractproperty

class K8sClusterResource(ABC):
    """
    A class which implement ClusterResource is a Terraform Ressource
    which managed a kubernetes cluster. It can be a self-managed cluster or a cluster
    provided by a cloud provider
    """

    @abstractproperty
    def services_cidr(self) -> str:
        """
        K8s internal network dedicated to services
        All traffic to these IP should be routed through the VPN
        """

    @abstractproperty
    def endpoint(self) -> str:
        """
        Public acessible endpoint where the k8s API is reachable
        """

    @abstractproperty
    def cluster_ca_certificate(self) -> str:
        """
        Cluster CA certificate to use to connect to the kubernetes cluster
        """

    @abstractproperty
    def token(self) -> str:
        """
        Auth token used to connect to the k8s serveur
        """
