from dataclasses import dataclass, field
from pprint import pformat, pprint
from typing import Dict, List, Optional


@dataclass
class ChallengeConfig:
    """Will be used to convert a YAML config file to an object we can manipulate using the `Challenge` class using `utility.ConfigLoader`
    """

    name: str
    description: str
    points: int
    category: str
    author: str
    has_files: bool
    has_container: bool
    files: List[str] = field(default_factory=list)
    ports: List[List[str, int]] = field(default_factory=list)

    def __repr__(self) -> str:
        """Repr method
        """
        return pformat(vars(self))
