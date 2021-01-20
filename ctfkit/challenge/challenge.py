from __future__ import annotations

from ctfkit.utility import ConfigLoader
from ctfkit.models import ChallengeConfig

class Challenge:
    """Handles Challenge objects to simplify data manipulation for challenges

    :param name: The name of the challenge
    :type name: str
    :param description: The description of the challenge
    :type description: str
    :param points: The number of points awarded when challenge is solved
    :type points: int
    :param category: 
    """

    def __init__(self, name: str, description: str, points: int, category: str, author: str, has_files: bool, has_container: bool, files=None, ports=None) -> None:
        """Constructor method
        """
        self.name = name
        self.description = description
        self.points = points
        self.category = category
        self.author = author
        self.has_files = has_files
        self.has_container = has_container
        self.files = files
        self.ports = ports

    def __str__(self):
        """String method
        """
        return f"""{self.name} - {self.points}pts ({self.author})"""

    @staticmethod
    def from_yaml(file: str) -> Challenge:
        """Returns a Challenge object by parsing a given yaml config file using a ConfigLoader. If the file is not valid, returns None
        You can find a challenge.yml example file at `/example/challenge/01-test/`

        :param file: The path to the yaml config file for a challenge
        :type file: str
        :return: The Challenge object corresponding to the config file, or None if the file is not valid
        :rtype: Challenge or None
        """

        try:
            # We parse the given file
            c = ConfigLoader(ChallengeConfig).convert(file)
            # Detect if extra files are used for the challenge
            has_files = len(c.files) > 0
            # Detect if challenge needs to be runned in a container
            has_container = len(c.container) > 0
            ports = None
            # Assign the given ports for the challenge object
            if has_container:
                ports = c.container
                
            return Challenge(c.name, c.description, c.points, c.category, c.author, has_files, has_container, files=c.files, ports=ports)
        except Exception as e:
            print(e)
            return None