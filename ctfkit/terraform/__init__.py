from os import getcwd
from subprocess import PIPE, Popen
from typing import List

from constructs import Construct
from cdktf import TerraformStack

from ctfkit.models import HostingEnvironment

class CtfStack(TerraformStack):
    """
    Root terraform stack which should contains every ressources
    needed to build up an infrastructure
    """
    def __init__(self, scope: Construct, environment: HostingEnvironment) -> None:
        super().__init__(scope, f'infra_{environment.value}')

    def init(self) -> None:
        process = Popen(['terraform', 'init'], cwd=getcwd() + '/.tfout', stderr=PIPE, stdout=PIPE, universal_newlines=True)
        return process.communicate()

    def plan(self) -> List[str]:
        process = Popen(['bash', '-c', 'terraform plan'], cwd=getcwd() + '/.tfout', stderr=PIPE, stdout=PIPE, universal_newlines=True)
        return process.communicate()
