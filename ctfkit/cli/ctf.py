import constructs
from cdktf import App
from ctfkit.terraform import CtfStack
from ctfkit.models.hosting_provider import HOSTING_PROVIDER
from click.core import Context
import click
from click.exceptions import BadParameter

from ctfkit.models import HOSTING_ENVIRONMENT, DeploymentConfig
from ctfkit.utility import ConfigLoader
from ctfkit.models import CtfConfig
from ctfkit.terraform.k8s_cluster import gcp


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
@click.argument('environment', required=True, type=click.Choice(map(lambda e: e.value, HOSTING_ENVIRONMENT)))
@pass_config
def plan(config: CtfConfig, environment: str):
    deployment_config: DeploymentConfig

    try:
        deployment_config = next(
            elem for elem in config.deployments if elem.environment.value == environment)

    except StopIteration:
        raise BadParameter(
            f'No deployment with the "{environment}" environment could be found in your configuration')

    app = App(outdir='.tfout')
    stack = CtfStack(app, deployment_config.environment.value)

    if deployment_config.provider == HOSTING_PROVIDER.GCP:
        gcp.GcpK8sCluster(stack, "cluster", config, deployment_config)

    app.synth()
