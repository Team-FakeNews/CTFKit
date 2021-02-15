from dataclasses import dataclass
from typing import List


@dataclass
class Member:
    name: str

@dataclass
class Team:
    name: str
    members: List[Member]
