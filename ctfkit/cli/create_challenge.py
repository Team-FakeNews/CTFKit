"""The project tree:

# Each challenge is an automaticaly generated git repo
challenge_1/
challenge_2/
...
# ctf-projet will be a git repo
/path/to/ctf-project/
    # Actual directory of the CTF
    ctf/
        ctf.yaml # The CTF's configuration
        # Will contain all the challenges decalred in the config file once the
        # CTF is started
        challenges/
"""
from os import getcwd, mkdir
from os.path import join
from git import Repo  # type: ignore

from ctfkit.utility import touch


def new_challenge(name: str) -> None:
    """Create a new challenge git repo for CTF Kit
    Each challenge is a git repo in the `your_project/dev/` directory, which
    CTF Kit will use to update your challenges
    TODO: write content of challenge.yaml on creation

    :param name: The name of the challenge
    :type name: str
    """
    path = getcwd()
    # Challenge's path will be /current/directory/challenge_name
    # TODO: But we will want to append a unique id to it
    challenge_path = join(path, name)
    print(f"Creating the repo for challenge {name}...")
    mkdir(challenge_path)

    # Init of the challenge git repo
    repo = Repo.init(challenge_path)

    """
    One challenge will be like so:

    /challenge_name/
        files/              # files for a challenge (image, text file given to
                            # players)
        src/                # source code of challenge
        challenge.yaml      # config file for the challenge
        flag                # text file containing the flag
        Dockerfile          # for production
        docker-compose.yml  # for testing locally
    """
    # We initiate the challenge's directory with default files
    default_dirs = ["files", "src"]
    default_files = ["challenge.yaml", "flag", "Dockerfile", "docker-compose.yml"]

    # Create all directories with .gitignore files to preserve them with commit
    for directory in default_dirs:
        path = join(challenge_path, directory)
        mkdir(path)
        file = join(path, ".gitignore")
        touch(file)

        repo.index.add(file)

    # Create all files and add them into the repo
    for default_file in default_files:
        touch(join(challenge_path, default_file))
    repo.index.add(default_files)

    repo.index.commit(f"CTF Kit challenge '{name}' initial commit")
    print(f"Done! You can check it at {challenge_path}")


def add_challenge(url: str) -> None:
    """Import a challenge with its URL

    :param url: The URL of the challenge (CTF Kit sub-module)
    """
    # TODO: check if the given URL is a local path or not to copy the files
    # without clonning a repo
    path = getcwd()
    # Challenge's path will be /current/directory/challenge_name
    target_dir = join(path, url.split('/')[-1])
    print(f"Challenge {url} will be imported in {target_dir}")
    mkdir(target_dir)
    Repo.clone_from(url, target_dir)
    print(f"Done! You can check it at {target_dir}")
