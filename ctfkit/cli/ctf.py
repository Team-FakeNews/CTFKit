from os import getcwd
from re import findall

import click
from click.core import Context
from yaspin import yaspin  # type: ignore
from yaspin.spinners import Spinners  # type: ignore

from ctfkit.models import CtfConfig, HostingEnvironment
from ctfkit.utility import ConfigLoader
from ctfkit.terraform import CtfDeployment


pass_config = click.make_pass_decorator(CtfConfig)


@click.group()
@click.option("--config",
              type=ConfigLoader(CtfConfig),
              default="ctf.yaml")
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

    helpers = TfHelpers(app)

    helpers.synth()
    helpers.init()
    helpers.plan()


@cli.command('deploy')
@click.argument('environment', required=True,
                type=click.Choice(map(lambda e: e.value, HostingEnvironment)))
@pass_config
def deploy(config: CtfConfig, environment: str):
    """
    Generate terraform configuration files
    from the ctf configuration and deploy required changes
    """

    # Find the requested environment
    environment_e = next(
        elem for elem in HostingEnvironment if elem.value == environment)

    # Declare out terraform stack
    app = CtfDeployment(config, environment_e, outdir=getcwd() + '/.tfout')
    helpers = TfHelpers(app)

    helpers.synth()
    helpers.init()
    helpers.deploy()


@cli.command('destroy')
@click.argument('environment', required=True,
                type=click.Choice(map(lambda e: e.value, HostingEnvironment)))
@pass_config
def destroy(config: CtfConfig, environment: str):
    """
    Generate terraform configuration files
    from the ctf configuration and deploy required changes
    """

    # Find the requested environment
    environment_e = next(
        elem for elem in HostingEnvironment if elem.value == environment)

    app = CtfDeployment(config, environment_e, outdir=getcwd() + '/.tfout')

    helpers = TfHelpers(app)

    helpers.synth()
    helpers.init()
    helpers.destroy()


class TfHelpers:
    """
    Infrastructure related helpers
    """

    infra: CtfDeployment

    def __init__(self, infra: CtfDeployment) -> None:
        self.infra = infra

    def init(self) -> None:
        """
        Wrap call to terraform init with a spinner
        """

        with yaspin(Spinners.dots12, text="Downloading modules ...") as spinner:
            _, stderr = self.infra.init()

            if len(stderr) > 0:
                spinner.fail(f"💥 {stderr}")
            else:
                spinner.ok("✅ ")

    def synth(self) -> None:
        """
        Wrap call to terraformcdk synth() method while showing a spinner
        """
        with yaspin(Spinners.dots12, text="Generating infrastructure configuration ...") as spinner:
            self.infra.synth()
            spinner.ok("✅ ")

    def plan(self) -> None:
        """
        Wrap call to terraform plan and show result on spinner
        """

        with yaspin(Spinners.dots12, text="Planning infrastructure ...") as spinner:
            result = self.infra.plan()
            if len(result[1]) > 0:
                spinner.fail("💥 ")
                print(result[1])

            else:
                spinner.ok("✅ ")
                print('\n'.join(findall(r'(.+resource "[^"]+" "[^"]+") \{', result[0])))

    def deploy(self) -> None:
        """
        Wrap call to terraform apply while showing stdout on a spinner
        """

        with yaspin(Spinners.dots12, text='Deploying infrastructure ... ') as spinner:
            stdout = self.infra.apply()
            if stdout is not None:
                for line in stdout:
                    if line != '':
                        spinner.text = "Deploying infrastructure ... " + line.strip('\n')

            spinner.ok("✅ ")

    def destroy(self) -> None:
        """
        Wrap a call to terraform destroy while showing stdout on a spinner
        """

        with yaspin(Spinners.dots12) as spinner:
            for line in self.infra.destroy():
                if line != '':
                    spinner.text = "Destroying infrastructure ... " + line.strip('\n')

            spinner.ok("✅ ")
