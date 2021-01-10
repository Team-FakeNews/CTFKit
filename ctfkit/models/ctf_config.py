from pprint import pformat, pprint
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from yaml import load, SafeLoader

from click import Path
from click.core import Context, Parameter
from slugify import slugify
from marshmallow_dataclass import class_schema

from ctfkit.utility import enum_to_regex
from .hosting_environment import HOSTING_ENVIRONMENT
from .hosting_provider import HOSTING_PROVIDER


@dataclass
class ClusterConfig:

    machine_type: str = 'n1-standard-4'
    node_count: int = 1

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass
class DeploymentConfig:

    environment: HOSTING_ENVIRONMENT = field(
        default=None, metadata={"by_value": True})
    provider: HOSTING_PROVIDER = field(
        default=None, metadata={"by_value": True})
    cluster: ClusterConfig = ClusterConfig()

    def __repr__(self) -> str:
        return pformat(vars(self), indent=4)


@dataclass
class CtfConfig():

    kind: str
    name: str
    challenges: List[str] = field(default_factory=list)
    deployments: List[DeploymentConfig] = field(default_factory=list)

    def getSlug(self) -> str:
        slugify(self.name)

    def __repr__(self) -> str:
        return pformat(vars(self))
