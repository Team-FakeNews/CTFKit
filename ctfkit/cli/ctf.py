from pprint import pformat, pprint
from typing import Callable
from click.core import Context

from ctfkit.utility import ConfigLoader
import click
from ctfkit.models import CtfConfig


pass_config = click.make_pass_decorator(CtfConfig)


@click.group()
@click.option("--config", type=ConfigLoader(CtfConfig), default="ctf.config.yaml")
@click.pass_context
def cli(context: Context, config: CtfConfig):
    context.obj = config


@cli.command('init')
def init():
    pass


@cli.command('plan')
@click.argument('environment', required=True)
@pass_config
def plan(config: CtfConfig, environment: str):
    pprint(config)
