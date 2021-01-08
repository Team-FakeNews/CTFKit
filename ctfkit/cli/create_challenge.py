"""The system tree for challenges:

# Each challenge is an automaticaly generated git repo
challenge_1/
challenge_2/
...
# ctf-projet will be a git repo
/path/to/ctf-project/
    # Actual directory of the CTF
    ctf/
        ctf.config
        # Will contain all the challenges decalred in the config file
        challenges/
"""

from ctfkit.utility import *


def new_challenge(name):
    """Create a new challenge git repo for CTF Kit
    Each challenge is a git repo in the `your_project/dev/` directory, which CTF kit will use to update your challenges

    :param name: The name of the challenge
    :type name: str
    """
    # We will want to first create a git repo for the CTF using the command `ctfkit ctf init`, and then create the challenges
    path = get_current_path()
    # Assuming the current directory has been checked using ctfkit.utility.check_installation()
    challenges_path = os.path.join(path, "challenges")
    # Challenge's directory will be `/path/to/challenge-name`
    # TODO: But we will want to append a unique id to it
    challenge_path = os.path.join(path, name)
    print(f"Creating the repo for challenge {name}...")
    mkdir(challenge_path)
    
    # TODO: Init of the challenge git repo

    """One challenge will be like so:

    /challenge_name/
        files/              # files for a challenge (image, text file given to players)
        src/                # source code of challenge
        flag                # text file containing the flag
        Dockerfile          # for production
        docker-compose.yml  # for testing locally
    """
    # We initiate the challenge's directory with default files
    default_dirs = ["files", "src"]
    default_files = ["flag", "Dockerfile", "docker-compose.yml"]

    # Create all directories
    for x in default_dirs:
        mkdir(os.path.join(challenge_path, x))

    # Create all files
    for x in default_files:
        touch(os.path.join(challenge_path, x))


def add_challenge(url):
    """Import a challenge with its URL

    :param url: The URL of the challenge (CTF Kit sub-module)
    :type url: str
    """
    # TODO: Paused for the moment
    print(f"Import challenge at {url}")
