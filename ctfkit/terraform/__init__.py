from os import getcwd
from os.path import join
from ctfkit.terraform.gcp import GcpGKE
from ctfkit.models.hosting_provider import HostingProvider
from ctfkit.models.ctf_config import CtfConfig, DeploymentConfig, GcpAuthConfig
from subprocess import PIPE, Popen
from typing import IO, List, Any, Mapping, Optional, Tuple

from constructs import Construct
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_google import GoogleProvider

from ctfkit.models import HostingEnvironment



class CtfDeployment(App):

    config: CtfConfig
    deployment_config: DeploymentConfig

    def __init__(
            self,
            config: CtfConfig,
            environment: HostingEnvironment,
            context: Mapping[str, Any] = None,
            outdir: str = None,
            stack_traces: bool = None) -> None:
        super().__init__(context=context, outdir=outdir, stack_traces=stack_traces)

        CtfStack(self, config, environment)

    def init(self) -> Tuple[str, str]:
        process = Popen(['terraform', 'init'], cwd=self.outdir, stderr=PIPE, stdout=PIPE, universal_newlines=True)
        return process.communicate()

    def plan(self) -> Tuple[str, str]:
        process = Popen(['terraform', 'plan'], cwd=self.outdir, stderr=PIPE, stdout=PIPE, universal_newlines=True)
        return process.communicate()

    def apply(self) -> Optional[IO[str]]:
        process = Popen(['terraform', 'apply', '-auto-approve'], cwd=self.outdir, stderr=PIPE, stdout=PIPE, universal_newlines=True)
        return process.stdout

    def destroy(self) -> Optional[IO[str]]:
        process = Popen(['terraform', 'destroy', '-auto-approve'], cwd=self.outdir, stderr=PIPE, stdout=PIPE, universal_newlines=True)
        return process.stdout


class CtfStack(TerraformStack):
    """
    Root terraform stack which should contains every ressources
    needed to build up an infrastructure
    """
    def __init__(
            self,
            scope: Construct,
            config: CtfConfig,
            environment: HostingEnvironment) -> None:
        super().__init__(scope, f'infra_{environment.value}')
        self.config = config
        self.deployment_config = config.get_deployment(environment)

        if self.deployment_config.provider == HostingProvider.GCP:
            self.__declare_gcp_cluster()

    def __declare_gcp_cluster(self) -> None:
        """
        Configure Google Cloud Platform's provider with provided credentials
        :private:
        """
        if self.deployment_config.gcp is None:
            raise TypeError('gcp config should not be empty')
            
        with open(self.deployment_config.gcp.credentials_file, 'r') as credentials:
            GoogleProvider(
                self,
                'gcp',
                credentials=credentials.read(),
                project=self.deployment_config.gcp.project,
                region=self.deployment_config.gcp.region,
                zone=self.deployment_config.gcp.zone
            )


        GcpGKE(self, 'k8s_cluster', self.deployment_config.cluster)
