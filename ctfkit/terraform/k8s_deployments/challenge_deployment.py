from cdktf import Resource
from cdktf_cdktf_provider_kubernetes import Deployment, DeploymentMetadata, DeploymentSpec, DeploymentSpecSelector, DeploymentSpecTemplate, DeploymentSpecTemplateMetadata, DeploymentSpecTemplateSpec, DeploymentSpecTemplateSpecContainer, DeploymentSpecTemplateSpecContainerPort, Service, ServiceMetadata, ServiceSpec, ServiceSpecPort
from constructs import Construct

from ctfkit.models import ChallengeConfig



class K8sChallengeDeployment(Resource):
    """
    Create a kubernetes deployment for the provided challenge
    """

    def __init__(
            self,
            scope: Construct,
            challenge_config: ChallengeConfig,
            namespace: str) -> None:
        super().__init__(scope, challenge_config.slug)

        Deployment(
            self,
            f'challenge-{challenge_config.slug}',
            metadata=[DeploymentMetadata(
                name=f'challenge-{challenge_config.slug}',
                namespace=namespace,
                labels={
                    'chall': challenge_config.slug
                }
            )],

            spec=[DeploymentSpec(
                selector=[DeploymentSpecSelector(
                    match_labels={
                        'chall': challenge_config.slug
                    }
                )],
                template=[DeploymentSpecTemplate(
                    metadata=[DeploymentSpecTemplateMetadata(
                        name=challenge_config.slug,
                        labels={
                            'chall': challenge_config.slug
                        }
                    )],
                    spec=[DeploymentSpecTemplateSpec(
                        container=[DeploymentSpecTemplateSpecContainer(
                            name=challenge_config.slug,
                            image_pull_policy='Always',
                            image=container_config.image,
                            port=[
                                DeploymentSpecTemplateSpecContainerPort(
                                    container_port=port_config.port,
                                    protocol=port_config.proto
                                )
                                for port_config in container_config.ports
                            ]
                        ) for container_config in challenge_config.containers]
                    )]
                )]
            )]
        )

        Service(
            self,
            'challenge',
            metadata=[ServiceMetadata(
                name=challenge_config.slug,
                namespace=namespace
            )],
            spec=[ServiceSpec(
                port=[
                    ServiceSpecPort(
                        name=f'port-{port_config.port}',
                        port=port_config.port,
                        target_port=f'{port_config.port}',
                        protocol=port_config.proto
                    ) for port_config in challenge_config.containers[0].ports
                ],
                selector={
                    'chall': challenge_config.slug
                }
            )]
        )