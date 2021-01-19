import sys
from ctfkit.terraform.k8s_cluster.gcp import GcpK8sCluster
from ctfkit.models.hosting_provider import HostingProvider
from ctfkit.models.ctf_config import CtfConfig, DeploymentConfig, GcpAuthConfig
from os import getcwd
from subprocess import PIPE, Popen
from typing import IO, List, Any, Mapping, Optional

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

    def init(self) -> List[str]:
        process = Popen(['terraform', 'init'], cwd=getcwd() + '/.tfout', stderr=PIPE, stdout=PIPE, universal_newlines=True)
        return process.communicate()

    def plan(self) -> List[str]:
        process = Popen(['bash', '-c', 'terraform plan'], cwd=getcwd() + '/.tfout', stderr=PIPE, stdout=PIPE, universal_newlines=True)
        return process.communicate()

    def apply(self) -> IO[str]:
        process = Popen(['bash', '-c', 'terraform apply -auto-approve'], cwd=getcwd() + '/.tfout', stderr=PIPE, stdout=PIPE, universal_newlines=True)
        return process.stdout

    def destroy(self) -> IO[str]:
        process = Popen(['bash', '-c', 'terraform destroy -auto-approve'], cwd=getcwd() + '/.tfout', stderr=PIPE, stdout=PIPE, universal_newlines=True)
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

        with open(self.deployment_config.gcp.credentials_file, 'r') as credentials:
            GoogleProvider(
                self,
                'gcp',
                credentials=credentials.read(),
                project=self.deployment_config.gcp.project,
                region=self.deployment_config.gcp.region,
                zone=self.deployment_config.gcp.zone
            )


        GcpK8sCluster(self, 'k8s_cluster', self.deployment_config.cluster)
