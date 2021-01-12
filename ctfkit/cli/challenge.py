import click
import docker
from yaspin import yaspin
import time
import traceback

@click.group()
def cli():
    pass

@cli.command('init')
def init():
    pass

@cli.command('run_challenge')
@click.argument('challenge', required=True)
def run_challenge(challenge):
    #Check if the given challenge exists

    try:
        #instance of the docker env
        client = docker.from_env()
    except:
            print("\n❌ Error, please check that Docker is installed and that your user has the proper rights to run it. :\n")
            traceback.print_exc()
    #build the docker image
    #tmp_challenge_path TMP !!!!
    tmp_challenge_path = "./"+challenge
    image_name = "ctfkit:"+challenge
    with yaspin(text="Starting challenge "+challenge, color="cyan") as sp:
        try:
            client.images.build(path=tmp_challenge_path, rm=True, forcerm=True, tag=image_name)
            time.sleep(0.5)
            sp.write("✔ Image building")
        except:
            time.sleep(0.5)
            print("\n❌ Error while building Docker Image, please check if a Dockerfile exists and if it's correct :\n")
            traceback.print_exc()
            exit(1)
        try:
            client.containers.run(image_name, auto_remove=True, detach=True, name="ctfkit_"+challenge)
            sp.ok("✔")
        except:
            time.sleep(0.5)
            print("\n❌ Error, unable to run a Docker container based on the image "+image_name+" :\n")
            traceback.print_exc()
            exit(1)

@cli.command('stop_challenge')
@click.argument('challenge', required=True)
def stop_challenge(challenge):
    #Check if the given challenge exists
    #Check if the given challenge is running

    try:
        #instance of the docker env
        client = docker.from_env()
    except:
            print("\n❌ Error, please check that Docker is installed and that your user has the proper rights to run it. :\n")
            traceback.print_exc()
            exit(1)
    container_name = "ctfkit_"+challenge
    with yaspin(text="Starting challenge "+challenge, color="cyan") as sp:
        #Get the container related to the challenge
        try:
            container = client.containers.get(container_name)
        except:
            time.sleep(0.5)
            print("\n❌ Error, please check that the supplied challenge is running :\n")
            traceback.print_exc()
            exit(1)
        #Stop the container
        try:
            container.stop()
        except:
            time.sleep(0.5)
            print("\n❌ Error, unable to stop the Docker container :\n")
            traceback.print_exc()
            exit(1)
        time.sleep(0.5)
        sp.write("✔ Challenge stopping")
        #remove the related image
        try:
            client.images.remove(image=container.image.id, force=True)
        except:
            time.sleep(0.5)
            print("\n❌ Error, unable to remove the Docker image related to the challenge :\n")
            traceback.print_exc()
            exit(1)
        time.sleep(0.5)
        sp.write("✔ Image removing")
        sp.ok("✔")