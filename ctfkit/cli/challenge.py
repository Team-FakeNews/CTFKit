# TODO: use a proper function to retrieve docker from env (declare in utility.py?)
import sys
from os import getcwd

import click
import docker  # type: ignore
from yaspin import yaspin  # type: ignore

from ctfkit.utility import is_slug, is_url
from ctfkit.cli.create_challenge import add_challenge, new_challenge
from ctfkit.constants import SPINNER_MODEL, SPINNER_FAIL, SPINNER_SUCCESS


@click.group()
def cli() -> None:
    pass


@cli.command('run')
@click.argument('challenge', required=True)
def run(challenge: str) -> None:
    """Run a challenge inside a Docker container.
    For the moment this method doesn't add any specific parameters to the
    container (such as port) but it will when a challenge object will be
    available.
    First a Docker image is built using the Dockerfile located in the
    challenge's directory and then we run a Docker container with the built
    image.

    :param challenge: The name of the challenge to run
    """
    # TODO: Check if the challenge exists
    # TODO: Use a challenge object to get the information related to the challenge
    # such as path, parameters like required ports or volumes)
    try:
        # Instance of the docker environment
        client = docker.from_env()
    except Exception as error:
        print(error)
        sys.exit(1)

    # Build the docker image
    tmp_challenge_path = os.path.join(getcwd(), challenge)
    image_name = f"ctfkit:{challenge}"
    with yaspin(SPINNER_MODEL, text=f"Starting challenge '{challenge}'", color="cyan") as spinner:
        try:
            spinner.write("Building image...")
            client.images.build(
                path=tmp_challenge_path,
                rm=True, forcerm=True,
                tag=image_name)
            spinner.write("Running image...")
            client.containers.run(
                image_name,
                auto_remove=True,
                detach=True,
                name=f"ctfkit_{challenge}")
            spinner.ok(f"{SPINNER_SUCCESS} Container '{image_name}' is running!")
        except Exception as error:
            # TODO: use better error handling to display custom message
            print(error)
            spinner.fail(f"{SPINNER_FAIL} Error while building/running the Docker image")
            sys.exit(1)


@cli.command('stop')
@click.argument('challenge', required=True)
def stop(challenge: str) -> None:
    """Stop a challenge running inside a Docker container.
    First we stop the container using his name, then we delete the related
    Docker image.

    :param challenge: The name of the running challenge.
    """
    # TODO: Check if the challenge is running and if it's an existing challenge.
    # TODO: Use a challenge object to get the information related to the challenge
    # such as path, parameters like required ports or volumes)
    try:
        # Instance of the docker environment
        client = docker.from_env()
    except Exception as error:
        print(error)
        sys.exit(1)

    container_name = f"ctfkit_{challenge}"
    with yaspin(SPINNER_MODEL, text=f"Stopping challenge '{challenge}'...", color="cyan") as spinner:
        try:
            # Get the container related to the challenge
            container = client.containers.get(container_name)
            # Stop the container
            container.stop()
            # Remove the related image
            spinner.write("Removing image...")
            client.images.remove(
                image=container.image.id,
                force=True)
            spinner.ok(f"{SPINNER_SUCCESS} Image '{container_name}' successfully stopped and removed!")
        except Exception as error:
            print(error)
            spinner.fail(f"{SPINNER_FAIL} Error, unable to stop the Docker container '{container_name}'")
            sys.exit(1)


@cli.command('new')
@click.argument('challenge_name', nargs=1)
def new(challenge_name: str) -> None:
    """<challenge_name>: Creates a CTF Kit challenge repo for a new challenge

    :param challenge_name: The name of the challenge to create
    :type challenge_name: str
    """
    if is_slug(challenge_name):
        new_challenge(challenge_name)


@cli.command('add')
@click.argument('challenge_url', nargs=1)
def add(challenge_url: str) -> None:
    """<challenge_url>: Import a challenge with its URL (must be a GIT repo)

    :param challenge_url: The URL of the challenge to import
    :type challenge_url: str
    """
    if is_url(challenge_url):
        add_challenge(challenge_url)
