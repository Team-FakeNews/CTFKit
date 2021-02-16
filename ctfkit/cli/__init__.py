import click

from . import ctf, challenge


@click.group()
def root_cli():
    """
    Main cli which contains all sub-commands
    It doesn't do anything but showing help to the user
    """


root_cli.add_command(ctf.cli, 'ctf')
root_cli.add_command(challenge.cli, 'challenge')
