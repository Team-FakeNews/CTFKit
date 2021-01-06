import click
from . import ctf, challenge


@click.group()
def root_cli():
    pass


root_cli.add_command(ctf.cli, 'ctf')
root_cli.add_command(challenge.cli, 'challenge')
