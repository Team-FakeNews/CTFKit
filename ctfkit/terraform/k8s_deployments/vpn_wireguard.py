from base64 import b64encode
from cdktf import Resource
from cdktf_cdktf_provider_kubernetes import ConfigMap, ConfigMapMetadata, Deployment, DeploymentMetadata, DeploymentSpec, DeploymentSpecSelector, DeploymentSpecTemplate, DeploymentSpecTemplateMetadata, DeploymentSpecTemplateSpec, DeploymentSpecTemplateSpecContainer, DeploymentSpecTemplateSpecContainerEnv, DeploymentSpecTemplateSpecContainerPort, DeploymentSpecTemplateSpecContainerResources, DeploymentSpecTemplateSpecContainerSecurityContext, DeploymentSpecTemplateSpecContainerSecurityContextCapabilities, DeploymentSpecTemplateSpecContainerVolumeMount, DeploymentSpecTemplateSpecInitContainer, DeploymentSpecTemplateSpecInitContainerSecurityContext, DeploymentSpecTemplateSpecInitContainerSecurityContextCapabilities, DeploymentSpecTemplateSpecVolume, DeploymentSpecTemplateSpecVolumeConfigMap, DeploymentSpecTemplateSpecVolumeHostPath, Service, ServiceMetadata, ServiceSpec, ServiceSpecPort
from constructs import Construct
from ctfkit.models import Team
from hashlib import md5

class K8sVpnWireguard(Resource):

    config: str

    def __init__(
            self,
            scope: Construct,
            name: str,
            namespace: str,
            team: Team,
            domain: str,
            vpn_external_ip: str,
            port_index: int) -> None:
        super().__init__(scope, name)

        escaped_domain = domain.replace('.', '\\.')

        external_port = 51820 + port_index

        clients_config = '\n'.join([ f"""[Peer]
PublicKey = {b64encode(bytes(client.private_key.public_key)).decode()}
AllowedIPs = 10.8.8.{index+2}
""" for index, client in enumerate(team.members)])

        server_config = f"""[Interface]
# Adresse IP du serveur à l'intérieur du VPN
Address = 10.8.8.1/16
# Clef privée du serveur
PrivateKey = {b64encode(bytes(team.private_key)).decode()}
# Port sur lequel le serveur écoute
ListenPort = {external_port}


# On exécute les commandes d'ajout des règles lorsque le VPN démarre
PostUp = iptables -A FORWARD -i %i -j ACCEPT ; iptables -A FORWARD -o %i -j ACCEPT ; iptables -t nat -A POSTROUTING -s 10.8.8.0/16 -o eth0 -j MASQUERADE
# Et on rajoute des commandes pour les supprimer lorsque le VPN est éteint
PostDown = iptables -D FORWARD -i %i -j ACCEPT ; iptables -D FORWARD -o %i -j ACCEPT ; iptables -t nat -D POSTROUTING -s 10.8.8.0/16 -o eth0 -j MASQUERADE

{clients_config}
"""

        wg_config = ConfigMap(
            self,
            'wg_config',
            metadata=[ConfigMapMetadata(
                name='wg-config',
                namespace=namespace
            )],
            data={
                'wg0.conf': server_config
            }
        )

        
        coredns_config = ConfigMap(
            self,
            'coredns_config',
            metadata=[ConfigMapMetadata(
                name='corends-config',
                namespace=namespace
            )],
            data={
                'Corefile': f""".:53 {{
    log
    errors
    auto
    reload 10s
    rewrite stop {{
        name regex (.*)\.{escaped_domain} {{1}}.{namespace}.svc.cluster.local
        answer name (.*)\.{namespace}\.svc\.cluster\.local {{1}}.{domain}
    }}
    forward . /etc/resolv.conf
}}"""
            }
        )

        Deployment(
            self,
            'wireguard',
            metadata=[DeploymentMetadata(
                name='wireguard',
                namespace=namespace,
                labels={
                    'app': 'wireguard'
                },
                annotations={
                    'config_change': md5(server_config.encode()).hexdigest()
                }
            )],

            spec=[DeploymentSpec(
                selector=[DeploymentSpecSelector(
                    match_labels={
                        'app': 'wireguard'
                    }
                )],
                template=[DeploymentSpecTemplate(
                    metadata=[DeploymentSpecTemplateMetadata(
                        name='wireguard',
                        labels={
                            'app': 'wireguard'
                        }
                    )],
                    spec=[DeploymentSpecTemplateSpec(
                        init_container=[DeploymentSpecTemplateSpecInitContainer(
                            name='sysctl',
                            image='busybox',
                            command=[
                                'sh',
                                '-c',
                                'sysctl -w net.ipv4.ip_forward=1 && sysctl -w net.ipv4.conf.all.forwarding=1'
                            ],
                            security_context=[DeploymentSpecTemplateSpecInitContainerSecurityContext(
                                capabilities=[DeploymentSpecTemplateSpecInitContainerSecurityContextCapabilities(
                                    add=['NET_ADMIN']
                                )],
                                privileged=True
                            )]
                        )],

                        container=[
                            DeploymentSpecTemplateSpecContainer(
                                image='masipcat/wireguard-go:latest',
                                name='wireguard',
                                
                                resources=[DeploymentSpecTemplateSpecContainerResources(
                                    requests={
                                        'memory': '20M'
                                    }
                                )],
                                port=[DeploymentSpecTemplateSpecContainerPort(
                                    container_port=51820,
                                    protocol='UDP',
                                    name='wireguard'
                                )],
                                env=[DeploymentSpecTemplateSpecContainerEnv(
                                    name='LOG_LEVEL',
                                    value='debug'
                                )],
                                security_context=[DeploymentSpecTemplateSpecContainerSecurityContext(
                                    capabilities=[DeploymentSpecTemplateSpecContainerSecurityContextCapabilities(
                                        add=['NET_ADMIN']
                                    )]
                                )],
                                volume_mount=[
                                    DeploymentSpecTemplateSpecContainerVolumeMount(
                                        name='tun',
                                        mount_path='/dev/net/tun'
                                    ),

                                    DeploymentSpecTemplateSpecContainerVolumeMount(
                                        name='wg-cfgmap',
                                        mount_path='/etc/wireguard/wg0.conf',
                                        sub_path='wg0.conf'
                                    ),
                                ]
                            ),

                            DeploymentSpecTemplateSpecContainer(
                                image='coredns/coredns',
                                name='coredns',

                                args=['-conf', '/Corefile'],

                                volume_mount=[DeploymentSpecTemplateSpecContainerVolumeMount(
                                    name='coredns-cfgmap',
                                    mount_path='/Corefile',
                                    sub_path='Corefile'
                                )]
                            )
                        ],

                        volume=[
                            DeploymentSpecTemplateSpecVolume(
                                name='tun',
                                host_path=[DeploymentSpecTemplateSpecVolumeHostPath(path='/dev/net/tun')]
                            ),
                            DeploymentSpecTemplateSpecVolume(
                                name='wg-cfgmap',
                                config_map=[DeploymentSpecTemplateSpecVolumeConfigMap(
                                    name=wg_config.metadata_input[0].name
                                )]
                            ),
                            DeploymentSpecTemplateSpecVolume(
                                name='coredns-cfgmap',
                                config_map=[DeploymentSpecTemplateSpecVolumeConfigMap(
                                    name=coredns_config.metadata_input[0].name
                                )]
                            )
                        ]
                    )]
                )]
            )]
        )

        service = Service(
            self,
            'wireguard_front',
            metadata=[ServiceMetadata(
                name='wireguard-front',
                namespace=namespace
            )],
            wait_for_load_balancer=False,
            spec=[ServiceSpec(
                type='LoadBalancer',
                session_affinity='ClientIP',
                load_balancer_ip=vpn_external_ip,
                port=[ServiceSpecPort(
                    port=external_port,
                    protocol='UDP'
                )],
                selector={
                    'app': 'wireguard'
                }
            )]
        )

        self.endpoint_var = service.status('0').load_balancer[:-1] + '.0.ingress.0.ip}:' + str(external_port)
