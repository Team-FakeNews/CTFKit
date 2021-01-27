from __future__ import annotations

from ctfkit.utility import ConfigLoader
from ctfkit.models import ChallengeConfig


class Challenge:
    """
    Handles Challenge objects to simplify data manipulation for challenges and
    create challenges from a given config file
    """

    def __init__(self, config: ChallengeConfig) -> None:
        """ Constructor method """
        self.config = config

    def __str__(self) -> str:
        """ String method """
        return (f"{self.config.name} - {self.config.points}pts"
                f"({self.config.author})")

    @staticmethod
    def from_yaml(file: str) -> Challenge:
        """
        Returns a Challenge object by parsing a given yaml config file using
        a ConfigLoader. If the file is not valid, returns None
        You can find a challenge.yml example file at
        `/example/challenge/01-test/`

        :param file: The path to the yaml config file for a challenge
        :return: The Challenge object corresponding to the config file, or None
        if the file is not valid
        """

        # We parse the given file
        chall = ConfigLoader(ChallengeConfig).convert(file)
        # And create an instace of Challenge using the parsed file
        return Challenge(config=chall)
