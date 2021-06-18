from typing import List, Mapping, Optional
from cdktf import Resource
from cdktf_cdktf_provider_kubernetes import ConfigMap, ConfigMapMetadata, Deployment, DeploymentMetadata, DeploymentSpec, DeploymentSpecSelector, DeploymentSpecTemplate, DeploymentSpecTemplateMetadata, DeploymentSpecTemplateSpec, DeploymentSpecTemplateSpecContainer, DeploymentSpecTemplateSpecContainerEnv, DeploymentSpecTemplateSpecContainerPort, DeploymentSpecTemplateSpecContainerResources, DeploymentSpecTemplateSpecContainerVolumeMount, DeploymentSpecTemplateSpecImagePullSecrets, DeploymentSpecTemplateSpecVolume, DeploymentSpecTemplateSpecVolumeConfigMap, DeploymentSpecTemplateSpecVolumeConfigMapItems, Service, ServiceMetadata, ServiceSpec, ServiceSpecPort
from constructs import Construct
from slugify.slugify import slugify

from ctfkit.models import ChallengeConfig



class K8sChallengeDeployment(Resource):
    """
    Create a kubernetes deployment for the provided challenge
    """

    def __init__(
            self,
            scope: Construct,
            challenge_config: ChallengeConfig,
            namespace: str,
            image_pull_secret: Optional[str] = None) -> None:
        super().__init__(scope, challenge_config.slug)

        pull_secrets = [DeploymentSpecTemplateSpecImagePullSecrets(name=image_pull_secret)] if image_pull_secret is not None else []

        configs_map: List[Mapping[str, ConfigMap]] = []
        for index, container in enumerate(challenge_config.containers):
            configs_map.append({})
            for file in container.files:
                with open(file.local, 'r') as _file:
                    configs_map[index][file.local] = ConfigMap(
                        self,
                        'file-' + slugify(file.local),
                        metadata=[ConfigMapMetadata(
                            name='file-' + slugify(file.local),
                            namespace=namespace
                        )],
                        data={
                            'content': _file.read()
                        }
                    )

        Deployment(
            self,
            'deployment',
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
                        image_pull_secrets=pull_secrets,
                        container=[DeploymentSpecTemplateSpecContainer(
                            name=f'{challenge_config.slug}-{container_index}',
                            image_pull_policy='Always',
                            image=container_config.image,
                            port=[
                                DeploymentSpecTemplateSpecContainerPort(
                                    container_port=port_config.port,
                                    protocol=port_config.proto
                                )
                                for port_config in container_config.ports
                            ],
                            resources=[DeploymentSpecTemplateSpecContainerResources(
                                requests={
                                    'memory': container_config.resources.min_memory,
                                    'cpu': container_config.resources.min_cpu
                                },
                                limits={
                                    'memory': container_config.resources.max_memory,
                                    'cpu': container_config.resources.max_cpu
                                }
                            )],
                            
                            env=[DeploymentSpecTemplateSpecContainerEnv(
                                name=env_name,
                                value=env_value
                            ) for env_name, env_value in container_config.env.items()],

                            volume_mount=[DeploymentSpecTemplateSpecContainerVolumeMount(
                                name=configs_map[container_index][file.local].id[:-3] + 'metadata.0.name}',
                                mount_path=file.container,
                                sub_path='content'
                            ) for file in container_config.files]
                            # ) for key, cfg_map in configs_map[container_index].items()]
                        ) for container_index, container_config in enumerate(challenge_config.containers)],
                        volume=[DeploymentSpecTemplateSpecVolume(
                            name=cfg_map.id[:-3] + 'metadata.0.name}',
                            config_map=[DeploymentSpecTemplateSpecVolumeConfigMap(
                                name=cfg_map.id[:-3] + 'metadata.0.name}'
                            )]
                        ) for sublist in configs_map for key, cfg_map in sublist.items()]
                    )],
                )]
            )]
        )

        Service(
            self,
            'service',
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