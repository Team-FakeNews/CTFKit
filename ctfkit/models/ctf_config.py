from pprint import pformat
from typing import List
from dataclasses import dataclass, field

from slugify import slugify

from .hosting_environment import HostingEnvironment
from .hosting_provider import HostingProvider


@dataclass
class ClusterConfig:
    """
    Configuration model common to each cloud provider
    """
    machine_type: str = 'n1-standard-4'
    node_count: int = 1

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass
class DeploymentConfig:
    """
    The model of a deployment configuration.
    An environment is an infrastructure to be configured by ctfKit
    It can be either a private testing environment, or a production environment
    which should be the public and runing CTF.
    """
    environment: HostingEnvironment = field(
        default=None, metadata={"by_value": True})  # type: ignore
    provider: HostingProvider = field(
        default=None, metadata={"by_value": True})  # type: ignore
    cluster: ClusterConfig = ClusterConfig()

    def __repr__(self) -> str:
        return pformat(vars(self), indent=4)


@dataclass
class CtfConfig:
    """
    The root configuration of a CTF.
    It contains every each information which will be used by ctfkit
    in order the manage each environment.
    """
    kind: str
    name: str
    challenges: List[str] = field(default_factory=list)
    deployments: List[DeploymentConfig] = field(default_factory=list)

    def get_slug(self) -> str:
        """
        Slugified version of the ctf name
        """
        return slugify(self.name)

    def __repr__(self) -> str:
        return pformat(vars(self))
