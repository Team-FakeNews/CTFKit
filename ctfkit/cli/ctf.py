import click
import validators  # type: ignore
from cdktf import App
from click.exceptions import BadParameter
from git import Repo  # type: ignore
from os.path import join
from yaspin import yaspin  # type: ignore
from yaspin.spinners import Spinners  # type: ignore

from ctfkit.models import CtfConfig, DeploymentConfig, HostingEnvironment, HostingProvider
from ctfkit.terraform import CtfStack
from ctfkit.terraform.k8s_cluster import gcp
from ctfkit.utility import ConfigLoader, get_current_path, mkdir, touch

pass_config = click.make_pass_decorator(CtfConfig)


def check_ctf_name(name: str) -> bool:
    """
    Check if a given name is valid for a new CTF

    :param name: The name to check
    """
    if not validators.slug(name):
        print(f"'{name}' is not a valid name. You must supply a valid name for a"
        " new CTF (must be in a slug format)")
        return False
    else:
        return True


@click.group()
def cli():
    """ CTF generation/handling commands """
    pass


@cli.command('init')
@click.option("-n", "--ctf-name", type=str, prompt=True)
@click.option("--provider", type=str)
def init(ctf_name: str, provider: str) -> None:
    """
    Create the CTF repository in the current working directory

    :param ctf_name: The name of the CTF
    :param provider: The provider which will host the CTF
    """
    # Check if the given name is valid
    if not check_ctf_name(ctf_name):
        exit()

    path = get_current_path()
    ctf_path = join(path, ctf_name)

    # No provider provided
    if provider is None:
        provider = ""
    else:
        # Check if the given provider is valid
        allowed_providers = []
        for provider_ in HostingProvider:
            allowed_providers.append(provider_.value)

        # Get the provider until it is a valid one
        while provider not in allowed_providers:
            print(f"The provider must be one of : {allowed_providers}")
            provider = input("CTF provider (not case-sensitive): ").lower()

    # Create the CTF's directory
    print(f"Creating the repo for the CTF '{ctf_name}'...")
    mkdir(ctf_path)

    # Init the CTF git repo
    repo = Repo.init(ctf_path)

    """
    One CTF directory will be like so:

    /ctf_name/
        challenges/ # all challenges hosted on the CTF
        config/     # the configuration files of the CTF
        README.md   # a dummy README file to introduce the CTF
    """
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
@pass_config
def plan(config: CtfConfig, environment: str):
    """
    Generate terraform configuration files
    from the ctf configuration and plan required changes
    """
    deployment_config: DeploymentConfig

    # Find the requested environment
    try:
        deployment_config = next(
            elt for elt in config.deployments if elt.environment.value == environment)
    except StopIteration:
        raise BadParameter(f"No '{environment}' environment could be found in"
            "your configuration")

    # Declare out terraform stack
    app = App(outdir=join(getcwd(), "/.tfout"))
    stack = CtfStack(app, deployment_config.environment.value)

    if deployment_config.provider == HostingProvider.GCP:
        # Declare a GCP cluster while passing its configuration
        gcp.GcpK8sCluster(stack, "cluster", config, deployment_config)

    with yaspin(Spinners.dots12, text="Generating infrastructure configuration ...") as spinner:
        app.synth()
        spinner.ok("✅ ")
