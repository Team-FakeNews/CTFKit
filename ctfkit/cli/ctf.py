from os import getcwd
from re import findall

from cdktf import App
import click
from click.core import Context
from click.exceptions import BadParameter
from yaspin import yaspin  # type: ignore
from yaspin.spinners import Spinners  # type: ignore

from ctfkit.models import CtfConfig, DeploymentConfig, HostingEnvironment
from ctfkit.utility import ConfigLoader
from ctfkit.terraform import CtfDeployment



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
    """
    Generate terraform configuration files
    from the ctf configuration and plan required changes
    """

    environment_e = next(
        elem for elem in HostingEnvironment if elem.value == environment)

    # Declare out terraform stack
    app = CtfDeployment(config, environment_e, outdir=getcwd() + '/.tfout')

    with yaspin(Spinners.dots12, text="Generating infrastructure configuration ...") as spinner:
        app.synth()
        spinner.ok("✅ ")

    with yaspin(Spinners.dots12, text="Downloading modules ...") as spinner:
        result = app.init()
        if len(result[1]) > 0:
            spinner.fail(f"💥 {str(result[1])}")
        else:
            spinner.ok("✅ ")

    with yaspin(Spinners.dots12, text="Planning infrastructure ...") as spinner:
        result = app.plan()
        if len(result[1]) > 0:
            spinner.fail("💥 ")
            print(result[1])

        else:
            spinner.ok("✅ ")
            print('\n'.join(findall(r'(.+resource "[^"]+" "[^"]+") \{', result[0])))


@cli.command('deploy')
@click.argument('environment', required=True,
                type=click.Choice(map(lambda e: e.value, HostingEnvironment)))
@pass_config
def deploy(config: CtfConfig, environment: str):
    """
    Generate terraform configuration files
    from the ctf configuration and deploy required changes
    """

    environment_e = next(
        elem for elem in HostingEnvironment if elem.value == environment)

    # Declare out terraform stack
    app = CtfDeployment(config, environment_e, outdir=getcwd() + '/.tfout')

    with yaspin(Spinners.dots12, text="Generating infrastructure configuration ...") as spinner:
        app.synth()
        spinner.ok("✅ ")

    with yaspin(Spinners.dots12, text="Downloading modules ...") as spinner:
        result = app.init()
        if len(result[1]) > 0:
            spinner.fail(f"💥 {str(result[1])}")
        else:
            spinner.ok("✅ ")

    with yaspin(Spinners.dots12) as spinner:
        for line in app.apply():
            if line != '':
                spinner.text = "Deploying infrastructure ... " + line.strip('\n')
        # if len(result[1]) > 0:
        #     spinner.fail("💥 ")
        #     print(result[1])

        # else:
        spinner.ok("✅ ")
        #     print('\n'.join(findall(r'(.+resource "[^"]+" "[^"]+") \{', result[0])))


@cli.command('destroy')
@click.argument('environment', required=True,
                type=click.Choice(map(lambda e: e.value, HostingEnvironment)))
@pass_config
def destroy(config: CtfConfig, environment: str):
    """
    Generate terraform configuration files
    from the ctf configuration and deploy required changes
    """

    environment_e = next(
        elem for elem in HostingEnvironment if elem.value == environment)

    # Declare out terraform stack
    app = CtfDeployment(config, environment_e, outdir=getcwd() + '/.tfout')

    with yaspin(Spinners.dots12, text="Generating infrastructure configuration ...") as spinner:
        app.synth()
        spinner.ok("✅ ")

    with yaspin(Spinners.dots12, text="Downloading modules ...") as spinner:
        result = app.init()
        if len(result[1]) > 0:
            spinner.fail(f"💥 {str(result[1])}")
        else:
            spinner.ok("✅ ")

    with yaspin(Spinners.dots12) as spinner:
        for line in app.destroy():
            if line != '':
                spinner.text = "Destroying infrastructure ... " + line.strip('\n')
        # if len(result[1]) > 0:
        #     spinner.fail("💥 ")
        #     print(result[1])

        # else:
        spinner.ok("✅ ")
        #     print('\n'.join(findall(r'(.+resource "[^"]+" "[^"]+") \{', result[0])))
