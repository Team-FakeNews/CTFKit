from enum import Enum


class HostingProvider(Enum):
    """
    Represent a compatible hosting provider
    to which the configured infrastructure will be deployed
    """
    GCP: str = "gcp"
