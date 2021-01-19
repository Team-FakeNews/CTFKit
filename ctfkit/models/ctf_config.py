from pprint import pformat
from typing import List
from dataclasses import dataclass, field
from click.exceptions import BadParameter

from slugify import slugify

from .hosting_environment import HostingEnvironment
from .hosting_provider import HostingProvider


@dataclass
class GcpAuthConfig:
    project: str
    region: str
    zone: str
    credentials_file: str = 'credentials.json'

    def __repr__(self) -> str:
        return pformat(vars(self))


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
    gcp: GcpAuthConfig = None

    def __repr__(self) -> str:
        return pformat(vars(self), indent=4)


@dataclass
class CtfConfig():
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

    def get_deployment(self, environment: HostingEnvironment) -> DeploymentConfig:
        """
        Find the matching configuration matching the requested Environment
        :return: The environment config associated with the request environment
        """
        try:
            return next(
                elem for elem in self.deployments if elem.environment == environment)

        except StopIteration:
            raise BadParameter(f'No "{environment}" environment could be found in your configuration')

    def __repr__(self) -> str:
        return pformat(vars(self))
