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
              default="ctf.config.yml")
@click.pass_context
def cli(context: Context, config: CtfConfig):
    """CTF generation/handling commands"""
    context.obj = config


@cli.command('init')
@click.option("-n", "--ctf-name", type=str, prompt=True)
@click.option("--provider", type=click.Choice(map(lambda e: e.value, HostingEnvironment)))
def init(ctf_name: str, provider: HostingProvider):
    """Create the CTF repository in the current working directory

    :param ctf_name: The ctf_name of the CTF
    :type ctf_name: str

    :param provider: The provider which will host the CTF
    :type provider:
    """
    CONFIG: str = "/config"
    CHALLZ: str = "/challz"
    README: str = "/README.md"

    try:
        mkdir(ctf_name)
    except FileExistsError:
        return click.BadParameter(
                f"The directory of CTF {ctf_name} already exists"
            )

    PROVIDERS = [h.value.lower() for h in HOSTING_PROVIDER]
    if provider.lower() in PROVIDERS:
        return click.BadParameter(
                f"The provider must be one of them : {PROVIDERS}"
            )

    while provider.lower() not in PROVIDERS:
        provider = input(f"CTF provider (lowercase) {PROVIDERS} : ")

    mkdir(ctf_name + CHALLZ)
    mkdir(ctf_name + CONFIG)
    git.Repo.init(ctf_name)

    with open(ctf_name + README, 'r') as f:
        f.write(f"# {ctf_name}\n")


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
