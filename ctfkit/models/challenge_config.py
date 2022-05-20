from typing import List, Mapping, Optional
from dataclasses import dataclass, field
from pprint import pformat

from slugify import slugify

@dataclass
class PortConfig:
    """ Representing a port mapping for a challenge: protocol and number """

    proto: str
    port: int

    def __repr__(self):
        """ Repr method """
        return pformat(vars(self))

@dataclass
class FileConfig:
    local: str
    container: str


@dataclass
class ResourceConfig:
    min_memory: str
    max_memory: str
    min_cpu: str
    max_cpu: str


@dataclass
class ContainerConfig:
    """
    Represent the configuration of a the container which host the challenge
    """
    image: str
    resources: ResourceConfig
    ports: List[PortConfig] = field(default_factory=list)
    env: Mapping[str, str] = field(default_factory=dict)
    files: List[FileConfig] = field(default_factory=list)

@dataclass(repr=False)
class ChallengeConfig:
    """
    Will be used to convert a YAML config file to an object we can
    manipulate using the :class:`Challenge` class using :class:`utility.ConfigLoader`
    """

    name: str
    # description: str
    # points: int
    # category: str
    # author: str
    containers: List[ContainerConfig] = field(default_factory=list)
    # files: List[str] = field(default_factory=list)

    @property
    def slug(self) -> str:
        """
        Slugified version of the challenge's name
        """
        return slugify(self.name)

    @property
    def has_files(self) -> bool:
        """ Check if a challenge uses external files """
        return len(self.files) > 0

    @property
    def has_container(self) -> bool:
        """ Check if a challenge needs a container to run """
        return len(self.containers) > 0
