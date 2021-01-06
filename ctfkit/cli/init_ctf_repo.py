# coding: utf-8

"""The system tree for challenges:
/path/to/ctf-project/
	challenges/
"""

from ctfkit.utility import *

def new_challenge(name):
    """Create a new challenge sub-module for CTF Kit

    :param name: The name of the challenge
    :type name: str
    """
    print(f"New challenge {name}")
    path = get_current_path()
    # Assuming the current directory has been checked using ctfkit.utility.check_installation()
    challenges_path = os.path.join(path, "challenges")

def add_challenge(url):
    """Import a challenge with its URL

    :param url: The URL of the challenge (CTF Kit sub-module)
    :type url: str
    """
    print(f"Import challenge at {url}")
