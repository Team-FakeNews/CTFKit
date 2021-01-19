from os import getcwd
from cdktf import App
import click
from click.core import Context
from click.exceptions import BadParameter
from yaspin import yaspin  # type: ignore
from yaspin.spinners import Spinners  # type: ignore

from ctfkit.terraform import CtfStack
from ctfkit.models import CtfConfig, DeploymentConfig, HostingEnvironment, HostingProvider
from ctfkit.utility import ConfigLoader
from ctfkit.terraform.k8s_cluster import gcp


pass_config = click.make_pass_decorator(CtfConfig)


@click.group()
@click.option("--config",
              type=ConfigLoader(CtfConfig),
              default="ctf.config.yaml")
@click.pass_context
def cli(context: Context, config: CtfConfig):
    """Root group for the ctf command"""
    context.obj = config


@cli.command('init')
def init():
    """Init command
    TODO : Not implemented
    """


@cli.command('plan')
@click.argument('environment', required=True,
                type=click.Choice(map(lambda e: e.value, HostingEnvironment)))
@pass_config
def plan(config: CtfConfig, environment: str):
    """Generate terraform configuration files
    from the ctf configuration and plan required changes
    """
    deployment_config: DeploymentConfig

    # Find the requested environment
    try:
        deployment_config = next(
            elem for elem in config.deployments if elem.environment.value == environment)

    except StopIteration:
        raise BadParameter(f'No "{environment}" environment could be found in your configuration')

    # Declare out terraform stack
    app = App(outdir=getcwd() + '/.tfout')
    stack = CtfStack(app, deployment_config.environment.value)

    if deployment_config.provider == HostingProvider.GCP:
        # Declare a GCP cluster while passing its configuration
        gcp.GcpK8sCluster(stack, "cluster", config, deployment_config)

    with yaspin(Spinners.dots12, text="Generating infrastructure configuration ...") as spinner:
        app.synth()
        spinner.ok("✅ ")
