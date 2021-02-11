import sys
from subprocess import PIPE, Popen
from typing import IO, Any, Mapping, Tuple

from constructs import Construct
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_google import GoogleProvider
from cdktf_cdktf_provider_kubernetes import KubernetesProvider

from ctfkit.terraform.gcp import GcpGKE
from ctfkit.models.hosting_provider import HostingProvider
from ctfkit.models.ctf_config import CtfConfig, DeploymentConfig, GcpAuthConfig
from ctfkit.models import HostingEnvironment
from .challenge_deployment import ChallengeDeployment

class CtfDeployment(App):
    """
    Root application module which deploy the entire CTF infrastructure
    The infrastructure is build dynamically using the configuration provided by the user
    """

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
        """
        Wrap the execution of the terraform init command
        """
        process = Popen(
            ['terraform', 'init'],
            cwd=self.outdir,
            stderr=PIPE,
            stdout=PIPE,
            universal_newlines=True
        )
        return process.communicate()

    def plan(self) -> Tuple[str, str]:
        """
        Wrap the execution of the terraform plan command
        """
        process = Popen(
            ['terraform', 'plan'],
            cwd=self.outdir,
            stderr=PIPE,
            stdout=PIPE,
            universal_newlines=True
        )
        return process.communicate()

    def apply(self) -> IO[str]:
        """
        Wrap the execution of the terraform apply command
        """
        process = Popen(
            ['terraform', 'apply', '-auto-approve'],
            cwd=self.outdir,
            stderr=PIPE,
            stdout=PIPE,
            universal_newlines=True
        )
        assert process.stdout is not None

        return process.stdout

    def destroy(self) -> IO[str]:
        """
        Wrap the execution of the terraform destroy command
        """
        process = Popen(
            ['terraform', 'destroy', '-auto-approve'],
            cwd=self.outdir,
            stderr=PIPE,
            stdout=PIPE,
            universal_newlines=True
        )
        assert process.stdout is not None

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
            cluster = self._declare_gcp_cluster()
        else:
            raise Exception(f'Bad Hosting provider: {self.deployment_config.provider}')

        # Kubernetes provider configuration using previously configured cluster
        KubernetesProvider(
            self,
            'k8s_provider',
            host=cluster.endpoint.value
        )

        for challenge_config in config.get_challenges_config():
            ChallengeDeployment(self, challenge_config)


    def _declare_gcp_cluster(self) -> GcpGKE:
        """
        Configure Google Cloud Platform's provider with provided credentials
        :private:
        """
        if self.deployment_config.gcp is None:
            raise TypeError('gcp config should not be empty')

        try:
            with open(self.deployment_config.gcp.credentials_file, 'r') as credentials:
                GoogleProvider(
                    self,
                    HostingProvider.GCP.value,
                    credentials=credentials.read(),
                    project=self.deployment_config.gcp.project,
                    region=self.deployment_config.gcp.region,
                    zone=self.deployment_config.gcp.zone
                )

        except FileNotFoundError:
            print(f'ERROR: You are missing a {self.deployment_config.gcp.credentials_file}'
                  'to authenticate with GCP')
            sys.exit(1)

        return GcpGKE(self, 'k8s_cluster', self.deployment_config.cluster)
