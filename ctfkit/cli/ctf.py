import click
from ctfkit.cli.models import CtfConfig


@click.group()
@click.option("--config", type=CtfConfig(), default="ctf.config.yaml")
def cli(config):
    print(config)


@cli.command('init')
def init():
    pass


@cli.command('genconfig')
def generate_config():
    pass
