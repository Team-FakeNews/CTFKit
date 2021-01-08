"""This file includes -- as the name says -- utility functions, such as conversions, path-related operations, common checks...
"""

import os
from enum import Enum


def get_current_path():
    """Returns the current path in the system

    :return: The path of the current directory in the system
    :rtype: str
    """
    return os.path.abspath(".")


def touch(file, data=None):
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


def mkdir(dir):
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


def check_installation():
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
