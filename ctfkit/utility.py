"""This file includes -- as the name says -- utility functions, such as conversions, path-related operations, common checks...
"""

from inspect import Parameter
from json import loads
import os
from enum import Enum
from typing import Dict, Optional

from click import Path
from click.core import Context
from marshmallow.schema import Schema
from marshmallow.utils import pprint
from marshmallow_dataclass import class_schema
from yaml import load, safe_load
from yaml.loader import SafeLoader


class ConfigLoader(Path):
    base_cls: type

    def __init__(self, base_cls: type) -> None:
        super().__init__(exists=True, file_okay=True, dir_okay=False, readable=True)
        self.base_cls = base_cls

    def convert(self, value: str, param: Optional[Parameter], ctx: Optional[Context]) -> Path:
        # Load raw config using the default implementation from click
        config_content: str = super().convert(value, param, ctx)

        # Parse YAML
        config_yaml = load(open(config_content), Loader=SafeLoader)

        # Generate the marshmallow schema using the dataclass typings
        config_schema: Schema = class_schema(self.base_cls)()

        # Cast the dict to a real CtfConfig instance
        config: self.base_cls = config_schema.load(config_yaml)

        return config


def get_current_path() -> str:
    """Returns the current path in the system

    :return: The path of the current directory in the system
    :rtype: str
    """
    return os.path.abspath(".")


def touch(file: str, data=None) -> None:
    """Creates a file if it does not already exists, and write the content of `data` in it

    :param file: The file to create
    :type file: str
    :param data: The data to write into `file`
    :type data: str
    """
    if os.path.exists(file):
        print(f"File {file} already exists")
    else:
        f = open(file, "w")
        # If data has been specified
        if data:
            f.write(data)

        f.close()


def mkdir(dir: str) -> None:
    """Creates a directory if it does not already exists

    :param dir: The directory to create
    :type dir: str
    """
    if os.path.exists(dir) and os.path.isdir(dir):
        print(f"Directory {dir} already exists")
    else:
        try:
            os.mkdir(dir)
        except OSError as e:
            print(e)


def check_installation() -> None:
    """Checks the installation of CTF Kit on system (ie. are all files here?)
    For the moment, only the challenges/ directory is checked
    """
    path = get_current_path()
    is_challenges = False

    # Checking if challenges/ exists and is a directory
    challenges = os.path.join(path, "challenges")
    if os.path.exists(challenges) and os.path.isdir(challenges):
        is_challenges = True

    # Printing a message
    if is_challenges:
        print("Installation is complete! You can use CTF Kit correctly")
    else:
        print("CTF Kit is not installed correctly, you may have to initiate ctfkit again")


def enum_to_regex(enum: Enum) -> str:
    """Create a regex which match the provided enumerations

    :return: A regex matching any of the enumeration's values
    :rtype: str
    """
    return r"^(" + r"|".join(list(map(lambda symbol: symbol.value, enum))) + r")$"
