"""This file includes -- as the name says -- utility functions, such as
conversions, path-related operations, common checks...
"""

import os
import selectors
from dataclasses import is_dataclass
from io import StringIO
from subprocess import PIPE, Popen, STDOUT
from typing import Any, Callable, Generic, Optional, List, Tuple, Type, TypeVar

import validators  # type: ignore
from click import Path, Parameter
from click.core import Context
from marshmallow.schema import Schema
from marshmallow_dataclass import class_schema
from yaml import load
from yaml.loader import SafeLoader


ClassType = TypeVar('ClassType')


class ConfigLoader(Path, Generic[ClassType]):
    """
    Utility class to which parse, validate, and do marshmalling from a yaml
    file to the specified model class. The model must have the @dataclass
    decorator.
    The dataclass should carefully declare every attributes types which will
    allows to detemine the matching schema.

    :param base_cls: The dataclass which represent the yaml config to import
    """
    base_cls: Type[ClassType]

    def __init__(self, base_cls: Type[ClassType]) -> None:
        super().__init__(exists=True, file_okay=True, dir_okay=False, readable=True)

        if not is_dataclass(base_cls):
            raise ValueError('The base_cls argument my be a dataclass')

        self.base_cls = base_cls

    def convert(
            self,
            value: str,
            param: Optional[Parameter] = None,
            ctx: Optional[Context] = None) -> Any:
        """
        Reads the specified yaml file, then validate its schema and marshamall
        each value into a new instance of the previously provided class.

        :param path: Path to the yaml file
        :return: A new instance of the dataclass filled with attributes from
        the yaml file
        """
        # Load raw config using the default implementation from click
        config_content: str = super().convert(value, param, ctx)

        # Parse YAML
        with open(config_content) as file_hander:
            config_yaml = load(file_hander, Loader=SafeLoader)

        # Generate the marshmallow schema using the dataclass typings
        config_schema: Schema = class_schema(self.base_cls)()

        # Cast the dict to a real CtfConfig instance
        config = config_schema.load(config_yaml)

        return config


def get_current_path() -> str:
    """Use getcwd() from os instead
    Returns the current path in the system

    :return: The path of the current directory in the system
    :rtype: str
    """
    return os.path.abspath(".")


def proc_exec(
    args: List[str],
    cwd: Optional[str] = None,
    stdout_cb: Optional[Callable[[str], None]] = None,
    stderr_cb: Optional[Callable[[str], None]] = None) -> Tuple[str, str, int]:

    """Helps to handle multiple outputs which result from a process execute
    It can be use to receive multiple output concurrently using callbacks.
    Or it can be used to read outputs after the process completion.

    :param args: Process and its arguments, as if you were using Popen
    :param cwd: Optional direction where to run the process from
    :param stdout_cb: Optional callback function which will be called on each
    new line emitted on stdout
    :param stderr_cb: Optional callback function which will be called on each
    new line emitted on stderr
    :return: A tuple which container the complete stdout, stderr buffer and
    the exit code of the process
    """

    process = Popen(
        args,
        cwd=cwd,
        stderr=PIPE,
        stdout=PIPE,
        universal_newlines=True
    )

    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, stdout_cb)
    selector.register(process.stderr, selectors.EVENT_READ, stderr_cb)

    # Create buffer to accumulates outputs
    stdout_buf = StringIO()
    stderr_buf = StringIO()

    while process.poll() is None:
        events = selector.select()
        for key, _ in events:
            line = key.fileobj.readline()

            if key.fileobj is process.stdout:
                stdout_buf.write(line)
            elif key.fileobj is process.stderr:
                stderr_buf.write(line)
            else:
                raise Exception('Unexpected error : unable to determine the corresponding output')

            key.data(line)

    # Returns (stdout, stderr, exit_code)
    return stdout_buf.getvalue(), stderr_buf.getvalue(), process.wait()


def touch(path: str, data=None) -> None:
    """Creates a file if it does not already exists, and write the content of
    `data` in it

    :param file: The file to create
    :type file: str
    :param data: The data to write into `file`
    :type data: str
    """
    if os.path.exists(path):
        print(f"File {path} already exists")
    else:
        file = open(path, "w")
        # If data has been specified
        if data:
            file.write(data)

        file.close()


def mkdir(path: str) -> None:
    """Creates a directory if it does not already exists

    :param path: The directory to create
    """
    if os.path.exists(path) and os.path.isdir(path):
        print(f"Directory {path} already exists")
    else:
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)
            raise error


def is_slug(string: str) -> bool:
    """Checks if the given string is in a slug format

    :param string: The string to check
    """
    if not validators.slug(string):
        print(f"'{string}' is not valid. You must supply a slug-formatted string")
        return False

    return True


def is_url(string: str) -> bool:
    """Check if a given string is a valid URL

    :param url: The URL to check
    :return: True if the given URL is valid, False else
    """
    if not validators.url(string):
        print(f"{string} is not a valid URL. You must supply a valid URL (http:// or https://)")
        return False

    return True


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
