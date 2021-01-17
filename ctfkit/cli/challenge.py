import click
import docker
from yaspin import yaspin
import ctfkit.utility

@click.group()
def cli():
    pass


@cli.command('init')
def init():
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
    tmp_challenge_path = ctfkit.utility.get_current_path()+"/"+challenge
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