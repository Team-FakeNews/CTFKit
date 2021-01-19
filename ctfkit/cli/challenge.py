import click
import docker  # type: ignore
from yaspin import yaspin  # type: ignore
import ctfkit.utility
import os
import validators  # type: ignore
from . import create_challenge


def check_challenge_name(name: str) -> bool:
    """Check if a given name is valid for a new challenge

    :param name: The name to check
    :type name: str
    :return: True if the given name is valid, False else
    :rtype: bool
    """
    if not validators.slug(name):
        print(f"{name} is not a valid name. You must supply a valid name for a new challenge (must be a slug format)")
        return False
    else:
        return True


def check_challenge_url(url: str) -> bool:
    """Check if a given URL is valid for a challenge import

    :param url: The URL to check
    :type url: str
    :return: True if the given URL is valid, False else
    :rtype: bool
    """
    if not validators.url(url):
        print(f"{url} is not a valid URL. You must supply a valid URL for a challenge import (http:// or https://)")
        return False
    else:
        return True


@click.group()
def cli() -> None:
    pass


@cli.command('run')
@click.argument('challenge', required=True)
def run(challenge: str) -> None:
    """Run a challenge inside a Docker container.
    For the moment this method doesn't add any specific parameters to the container (such as port) but it will when a challenge object will be available.
    First a Docker image is build using the Dockerfile located in the challenge's directory and then run a Docker container with the builded image.

    :param challenge: The name of the challenge to run
    :type file: str
    """
    """TODO:
        Check if the challenge exists
        Use a challenge object to get the information related to the challenge such as path, parameters like required ports or volumes)
    """
    try:
        # Instance of the docker environment
        client = docker.from_env()
    except:
        print("\n❌ Error, please check that Docker is installed and that your user has the proper rights to run it.")
    # Build the docker image
    tmp_challenge_path = os.path.join(ctfkit.utility.get_current_path(), challenge)
    image_name = f"ctfkit:{challenge}"
    with yaspin(text=f"Starting challenge {challenge}", color="cyan") as sp:
        try:
            client.images.build(
                path=tmp_challenge_path,
                rm=True, forcerm=True,
                tag=image_name)
            sp.write("✔ Building image")
        except:
            print("\n❌ Error while building the Docker image, please check if a Dockerfile exists and if it's correct.")
            exit(1)
        try:
            client.containers.run(
                image_name,
                auto_remove=True,
                detach=True,
                name=f"ctfkit_{challenge}")
            sp.ok("✔")
        except:
            print(f"\n❌ Error, unable to run a Docker container based on the image {image_name}")
            exit(1)


@cli.command('stop')
@click.argument('challenge', required=True)
def stop(challenge: str) -> None:
    """Stop a challenge running inside a Docker container.
    First we stop the container using his name, then we delete the related Docker image.

    :param challenge: The name of the running challenge.
    :type file: str
    """
    """TODO:
        Check if the challenge is running and if it's an existing challenge.
        Use a challenge object to get the information related to the challenge such as path, parameters like required ports or volumes)
    """
    try:
        # Instance of the docker environment
        client = docker.from_env()
    except:
        print("\n❌ Error, please check that Docker is installed and that your user has the proper rights to run it.")
        exit(1)
    container_name = f"ctfkit_{challenge}"
    with yaspin(text=f"Stopping challenge {challenge}", color="cyan") as sp:
        # Get the container related to the challenge
        try:
            container = client.containers.get(container_name)
        except:
            print(f"\n❌ Error, please check that the supplied challenge is running : {container_name}")
            exit(1)
        # Stop the container
        try:
            container.stop()
        except:
            print("\n❌ Error, unable to stop the Docker container :\n")
            exit(1)
        sp.write("✔ Stopping Docker container")
        # Remove the related image
        try:
            client.images.remove(
                image=container.image.id,
                force=True)
        except:
            print("\n❌ Error, unable to remove the Docker image related to the challenge :\n")
            exit(1)
        sp.write("✔ Removing image")
        sp.ok("✔")


@cli.command('new')
@click.argument('challenge_name', nargs=1)
def new(challenge_name: str) -> None:
    """<challenge_name>: Creates a CTF Kit challenge repo for a new challenge

    :param challenge_name: The name of the challenge to create
    :type challenge_name: str
    """
    if check_challenge_name(challenge_name):
        create_challenge.new_challenge(challenge_name)


@cli.command('add')
@click.argument('challenge_url', nargs=1)
def add(challenge_url: str) -> None:
    """<challenge_url>: Import a challenge with its URL (must be a GIT repo)

    :param challenge_url: The URL of the challenge to import
    :type challenge_url: str
    """
    if check_challenge_url(challenge_url):
        create_challenge.add_challenge(challenge_url)
