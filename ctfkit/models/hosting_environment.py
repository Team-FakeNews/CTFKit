from enum import Enum


class HostingEnvironment(Enum):
    """Represents all possible type of deployments"""

    TESTING = "testing"
    PRODUCTION = "production"
