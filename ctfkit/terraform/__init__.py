from ctfkit.terraform.k8s_deployments.vpn_wireguard import K8sVpnWireguard
import sys
import json
from os.path import join
from subprocess import PIPE, Popen
from typing import Callable, Dict, IO, Any, List, Mapping, Tuple
from constructs import Construct

# Terraform CDK and precompiled providers
from cdktf import App, TerraformOutput, TerraformStack
from cdktf_cdktf_provider_google import GoogleProvider
from cdktf_cdktf_provider_kubernetes import KubernetesProvider, Namespace, NamespaceMetadata
from cdktf_cdktf_provider_azurerm import AzurermProvider, AzurermProviderFeatures

from ctfkit.utility import proc_exec
from ctfkit.models.hosting_provider import HostingProvider
from ctfkit.models.ctf_config import CtfConfig, DeploymentConfig
from ctfkit.models import HostingEnvironment
from .k8s_deployments import K8sChallengeListDeployments
from .k8s_cluster import K8sClusterResource, AzureAKS, GcpGKE

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

    def plan(self, stdout_cb: Callable[[str], None]) -> Tuple[int, str, str]:
        """
        Wrap the execution of the terraform plan command
        """
        command = ['terraform', 'plan']
        return proc_exec(
            command,
            cwd=self.outdir,
            stdout_cb=stdout_cb,
            stderr_cb=lambda line: sys.stderr.write(f'[{" ".join(command)}: STDERR]: {line}')
        )

    def apply(self, stdout_cb: Callable[[str], None]) -> Tuple[int, str, str]:
        """
        Wrap the execution of the terraform apply command
        """
        command = ['terraform', 'apply', '-auto-approve']
        return proc_exec(
            command,
            cwd=self.outdir,
            stdout_cb=stdout_cb,
            stderr_cb=lambda line: sys.stderr.write(f'[{" ".join(command)}: STDERR]: {line}')
        )

    def destroy(self, stdout_cb: Callable[[str], None]) -> Tuple[int, str, str]:
        """
        Wrap the execution of the terraform destroy command
        """
        command = ['terraform', 'destroy', '-auto-approve']
        return proc_exec(
            command,
            cwd=self.outdir,
            stdout_cb=stdout_cb,
            stderr_cb=lambda line: sys.stderr.write(f'[{" ".join(command)}: STDERR]: {line}')
        )

    def get_outputs(self) -> List[Any]:
        return json.load(open(join(self.outdir, 'terraform.tfstate'), 'r'))['outputs']


class CtfStack(TerraformStack):
    """
    Root terraform stack which should contains every ressources
    needed to build up an infrastructure
    """

    servers: Dict[str, str] = {}

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

        elif self.deployment_config.provider == HostingProvider.AZURE:
            cluster = self._declare_azure_cluster()

        else:
            raise Exception(f'Unsupported Hosting provider: {self.deployment_config.provider}')

        # Kubernetes provider configuration using previously configured cluster
        KubernetesProvider(
            self,
            'kubernetes',
            host=cluster.endpoint,
            client_certificate=f'${{base64decode({cluster.client_certificate[2:-1]})}}',
            client_key=f'${{base64decode({cluster.client_key[2:-1]})}}',
            cluster_ca_certificate=f'${{base64decode({cluster.cluster_ca_certificate[2:-1]})}}'
        )

        if self.config.teams is not None:
            for team in self.config.teams:
                ns = Namespace(
                    self,
                    'team_ns',
                    metadata=[NamespaceMetadata(
                        name=f'team-{team.name}'
                    )]
                )

                self.servers[team.name] = K8sVpnWireguard(
                    self,
                    'team_wireguard',
                    ns.metadata_input[0].name,
                    team
                ).endpoint_var

                K8sChallengeListDeployments(self, 'team_challenges', self.config.challenges_config, ns.metadata_input[0].name)

        TerraformOutput(
            self,
            'servers',
            value=self.servers
        ).override_logical_id('servers')

    def _declare_gcp_cluster(self) -> K8sClusterResource:
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

        return GcpGKE(self, 'k8s_cluster', self.deployment_config.gcp)

    def _declare_azure_cluster(self) -> K8sClusterResource:
        AzurermProvider(self, HostingProvider.AZURE.value, features=[AzurermProviderFeatures()])

        return AzureAKS(self, 'k8s_cluster', self.deployment_config.azure)
