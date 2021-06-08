from dataclasses import dataclass, field
from typing import List, Optional

from nacl.public import PrivateKey  # type: ignore
from slugify import slugify


@dataclass
class Member:
    """
    Represent a member imported from a JSON file
    """
    name: str
    private_key: Optional[PrivateKey] = field(init=False)


@dataclass
class Team:
    """
    Represent a team imported from a JSON file
    """
    name: str
    members: List[Member]
    private_key: Optional[PrivateKey] = field(init=False)

    @property
    def slug(self) -> str:
        """
        Slugified team name compatible with k8s
        """
        return slugify(self.name)
