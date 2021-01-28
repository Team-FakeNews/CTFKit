from dataclasses import dataclass, field
from pprint import pformat
from typing import List


@dataclass
class PortConfig:
    """ Representing a port mapping for a challenge: protocol and number """

    proto: str
    port: int

    def __repr__(self):
        """ Repr method """
        return pformat(vars(self))


@dataclass
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
    files: List[str] = field(default_factory=list)
    container: List[PortConfig] = field(default_factory=list)

    def __repr__(self) -> str:
        """ Repr method """
        return pformat(vars(self))

    def has_files(self) -> bool:
        """ Check if a challenge uses external files """
        return len(self.files) > 0

    def has_container(self) -> bool:
        """ Check if a challenge needs a container to run """
        return len(self.container) > 0
