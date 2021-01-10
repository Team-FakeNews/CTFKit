from pprint import pformat, pprint
from ctfkit.utility import ConfigLoader
import click
from ctfkit.models import CtfConfig


@click.group()
@click.option("--config", type=ConfigLoader(CtfConfig), default="ctf.config.yaml")
def cli(config):
    pprint(config)


@cli.command('init')
def init():
    pass


@cli.command('genconfig')
def generate_config():
    pass
