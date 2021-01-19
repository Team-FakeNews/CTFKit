from __future__ import annotations

from strictyaml import load, Map, Str, Int, Seq  # type: ignore


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
        """Returns a Challenge object by parsing a given yaml config file
        You can find a challenge.yml example file at /example/challenge/01-test/
        For the moment this method uses strictyaml for ease, but a config loader will be implemented, see the code in 'TODO:' below

        :param file: The path to the yaml config file for a challenge
        :type file: str
        :return: The Challenge object corresponding to the config file
        :rtype: Challenge
        """
        """TODO: implement once the MR of this feature is accepted
        from ctfkit.utility import ConfigLoader
        from ctfkit.models import ChallengeConfig

        c = ConfigLoader(ChallengeConfig).convert(file)
        return Challenge(c.name, c.description, c.points, c.category, c.author, c.has_files, c.has_container, files=c.files, ports=c.ports)
        """
        yaml = open(file, "r").read()
        # Our schema with types
        data = load(yaml, Map({"name": Str(), "description": Str(), "points": Int(), "category": Str(
        ), "author": Str(), "files": Seq(Str()), "container": Seq(Map({"proto": Str(), "port": Int()}))}))

        # We retrieve values to build a Challenge object
        name = data["name"].value
        description = data["description"].value
        points = data["points"].value
        category = data["category"].value
        author = data["author"].value

        # Check if challenge needs files
        files = None
        has_files = False
        if len(data["files"]) >= 1 and data["files"][0].value != '':
            has_files = True
            # files will contain all given files for a challenge, such as files = ['index.php', 'background.jpg']
            files = []
            for x in data["files"]:
                files.append(x.value)

        # Check if challenge runs in a container
        container = data["container"]
        has_container = False
        ports = None
        if len(container) >= 1 and container[0]["proto"].value != '' and container[0]["port"].value != '':
            has_container = True
            # ports will contain a list of each ports for a challenge and its associated protocol, such as ports = [['tcp', 80], ['udp', 1337]]
            ports = []
            for x in container:
                ports.append([x["proto"].value, x["port"].value])

        return Challenge(name, description, points, category, author, has_files, has_container, files=files, ports=ports)
