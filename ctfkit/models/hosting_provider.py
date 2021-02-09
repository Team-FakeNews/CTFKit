from enum import Enum


class HostingProvider(Enum):
    """
    Represents a compatible hosting provider which the configured
    infrastructure will be deployed on
    """
    GCP: str = "gcp"
