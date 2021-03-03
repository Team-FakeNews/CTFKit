import git  # type: ignore
from os import getcwd
from os.path import join
from re import findall
import sys

import click
from click.core import Context
from yaspin import yaspin  # type: ignore

from ctfkit.constants import SPINNER_SUCCESS, SPINNER_FAIL, SPINNER_MODEL
from ctfkit.models import CtfConfig, HostingEnvironment, HostingProvider
from ctfkit.utility import ConfigLoader, mkdir, touch, is_slug
from ctfkit.terraform import CtfDeployment


@click.group()
@click.pass_context
def cli(context: Context):
    """Root group for the ctf command"""


@cli.command('init')
@click.option("-n", "--ctf-name", type=str, prompt=True)
@click.option('-p', '--provider', prompt=True,
              type=click.Choice(list(map(lambda e: e.value, HostingProvider))))
def init(ctf_name: str, provider: str) -> None:
    """
    Create the CTF repository in the current working directory

    :param ctf_name: The name of the CTF
    :param provider: The provider which will host the CTF
    """
    # Check if the given name is valid
    if not is_slug(ctf_name):
        sys.exit(1)

    path = getcwd()
    ctf_path = join(path, ctf_name)

    # Create the CTF's directory
    mkdir(ctf_path)

    # Init the CTF git repo
    repo = git.Repo.init(ctf_path)

    # One CTF directory will be like so:
    # /ctf_name/
    #     challenges/ # all challenges hosted on the CTF
    #     config/     # the configuration files of the CTF
    #     README.md   # a dummy README file to introduce the CTF

    # We initiate the CTF's directory with default files
    readme_default_file = "README.md"
    default_dirs = ["challenges", "config"]
    default_files = [readme_default_file]

    # Create all directories with .gitkeep file to preserve them if empty
    for default in default_dirs:
        dir_ = join(ctf_path, default)
        mkdir(dir_)
        gitkeep = join(dir_, ".gitkeep")
        touch(gitkeep)
        repo.index.add(gitkeep)

    # Create all files and add them into the repo
    for default in default_files:
        file_path = join(ctf_path, default)
        touch(file_path)
        # Fill the README file with default content
        if default == readme_default_file:
            with open(file_path, 'w') as file_:
                file_.write(f"# [CTF Kit] {ctf_name}\n")
    repo.index.add(default_files)

    repo.index.commit(f"CTF Kit ctf '{ctf_name}' initial commit")
    print(f"Done! You can check it at {ctf_path}")


@cli.command('plan')
@click.argument('environment', required=True,
                type=click.Choice(map(lambda e: e.value, HostingEnvironment)))
@click.option("--config",
              type=ConfigLoader(CtfConfig),
              default="ctf.yaml")
def plan(config: CtfConfig, environment: str):
    """
    Generate terraform configuration files
    from the ctf configuration and plan required changes
    """

    environment_e = next(
        elem for elem in HostingEnvironment if elem.value == environment)

    # Declare out terraform stack
    app = CtfDeployment(config, environment_e, outdir=join(getcwd(), '.tfout'))

    helpers = TfHelpers(app)

    helpers.synth()
    helpers.init()
    helpers.plan()


@cli.command('deploy')
@click.argument('environment', required=True,
                type=click.Choice(map(lambda e: e.value, HostingEnvironment)))
@click.option("--config",
              type=ConfigLoader(CtfConfig),
              default="ctf.yaml")
def deploy(config: CtfConfig, environment: str):
    """
    Generate terraform configuration files
    from the ctf configuration and deploy required changes
    """

    # Find the requested environment
    environment_e = next(
        elem for elem in HostingEnvironment if elem.value == environment)

    # Declare out terraform stack
    app = CtfDeployment(config, environment_e, outdir=join(getcwd(), '.tfout'))
    helpers = TfHelpers(app)

    helpers.synth()
    helpers.init()
    helpers.deploy()


@cli.command('destroy')
@click.argument('environment', required=True,
                type=click.Choice(map(lambda e: e.value, HostingEnvironment)))
@click.option("--config",
              type=ConfigLoader(CtfConfig),
              default="ctf.yaml")
def destroy(config: CtfConfig, environment: str):
    """
    Generate terraform configuration files
    from the ctf configuration and deploy required changes
    """

    # Find the requested environment
    environment_e = next(
        elem for elem in HostingEnvironment if elem.value == environment)

    app = CtfDeployment(config, environment_e, outdir=join(getcwd(), '.tfout'))

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

        with yaspin(SPINNER_MODEL, text="Downloading modules ...") as spinner:
            _, stderr = self.infra.init()

            if len(stderr) > 0:
                spinner.fail(SPINNER_FAIL + stderr)
            else:
                spinner.ok(SPINNER_SUCCESS)

    def synth(self) -> None:
        """
        Wrap call to terraformcdk synth() method while showing a spinner
        """
        with yaspin(SPINNER_MODEL, text="Generating infrastructure configuration ...") as spinner:
            self.infra.synth()
            spinner.ok(SPINNER_SUCCESS)

    def plan(self) -> None:
        """
        Wrap call to terraform plan and show result on spinner
        """

        with yaspin(SPINNER_MODEL, text="Planning infrastructure ...") as spinner:
            result = self.infra.plan()
            if len(result[1]) > 0:
                spinner.fail(SPINNER_FAIL)
                print(result[1])

            else:
                spinner.ok(SPINNER_SUCCESS)
                print(
                    '\n'.join(findall(r'(.+resource "[^"]+" "[^"]+") \{', result[0])))

    def deploy(self) -> None:
        """
        Wrap call to terraform apply while showing stdout on a spinner
        """

        with yaspin(SPINNER_MODEL, text='Deploying infrastructure ... ') as spinner:
            stdout = self.infra.apply()
            if stdout is not None:
                for line in stdout:
                    if line != '':
                        spinner.text = "Deploying infrastructure ... " + \
                            line.strip('\n')

            spinner.ok(SPINNER_SUCCESS)

    def destroy(self) -> None:
        """
        Wrap a call to terraform destroy while showing stdout on a spinner
        """

        with yaspin(SPINNER_MODEL) as spinner:
            for line in self.infra.destroy():
                if line != '':
                    spinner.text = "Destroying infrastructure ... " + \
                        line.strip('\n')

            spinner.ok(SPINNER_SUCCESS)
