from typing import List
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
class ContainerConfig:
    """
    Represent the configuration of a the container which host the challenge
    """
    image: str
    ports: List[PortConfig] = field(default_factory=list)


@dataclass(repr=False)
class ChallengeConfig:
    """
    Will be used to convert a YAML config file to an object we can
    manipulate using the `Challenge` class using `utility.ConfigLoader`
    """

    name: str
    description: str
    points: int
    category: str
    author: str
    containers: List[ContainerConfig] = field(default_factory=list)
    files: List[str] = field(default_factory=list)

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
