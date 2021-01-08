"""The system tree for challenges:

# Each challenge is an automaticaly generated git repo
challenge_1/
challenge_2/
...
# ctf-projet will be a git repo
/path/to/ctf-project/
    # Actual directory of the CTF
    ctf/
        ctf.yml # The CTF's configuration
        # Will contain all the challenges decalred in the config file once the CTF is started
        challenges/
"""

from git import Repo

from ctfkit.utility import *


def new_challenge(name):
    """Create a new challenge git repo for CTF Kit
    Each challenge is a git repo in the `your_project/dev/` directory, which CTF kit will use to update your challenges

    :param name: The name of the challenge
    :type name: str
    """
    path = get_current_path()
    # Challenge's path will be /current/directory/challenge_name
    # TODO: But we will want to append a unique id to it
    challenge_path = os.path.join(path, name)
    print(f"Creating the repo for challenge {name}...")
    mkdir(challenge_path)

    # Init of the challenge git repo
    repo = git.Repo.init(challenge_path)

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

    # Create all directories with .gitignore files to preserve them with commit
    for x in default_dirs:
        d = os.path.join(challenge_path, x)
        mkdir(d)
        f = os.path.join(d, ".gitignore")
        touch(f)
        repo.index.add(f)

    # Create all files and add them into the repo
    for x in default_files:
        touch(os.path.join(challenge_path, x))
    repo.index.add(default_files)

    repo.index.commit("CTF Kit challenge initial commit")
    print(f"Done! You can check it at {challenge_path}")


def add_challenge(url):
    """Import a challenge with its URL

    :param url: The URL of the challenge (CTF Kit sub-module)
    :type url: str
    """
    path = get_current_path()
    # Challenge's path will be /current/directory/challenge_name
    target_dir = os.path.join(path, url.split('/')[-1])
    print(f"Challenge {url} will be imported in {target_dir}")
    mkdir(target_dir)
    Repo.clone_from(url, target_dir)
    print(f"Done! You can check it at {target_dir}")
