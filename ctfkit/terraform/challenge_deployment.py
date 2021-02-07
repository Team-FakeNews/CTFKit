from cdktf import Resource
from cdktf_cdktf_provider_kubernetes import Deployment, DeploymentMetadata, DeploymentSpec, DeploymentSpecSelector, DeploymentSpecTemplate, DeploymentSpecTemplateMetadata, DeploymentSpecTemplateSpec, DeploymentSpecTemplateSpecContainer, DeploymentSpecTemplateSpecContainerPort
from constructs import Construct

from ctfkit.models import ChallengeConfig



class ChallengeDeployment(Resource):

    def __init__(self, scope: Construct, challenge_config: ChallengeConfig) -> None:
        super().__init__(scope, challenge_config.slug)

        Deployment(
            self,
            f'challenge_{challenge_config.slug}',
            metadata=[DeploymentMetadata(
                name=f'challenge_{challenge_config.slug}',
                # namespace='' TODO: Manage teams namespaces
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
