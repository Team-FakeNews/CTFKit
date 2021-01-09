from typing import Dict, List, Optional
from attr import dataclass
from yaml import load, SafeLoader

from click import Path
from click.core import Context, Parameter
from slugify import slugify
from marshmallow_dataclass import class_schema

from ctfkit.utility import enum_to_regex
from .hosting_environment import HOSTING_ENVIRONMENT
from .hosting_provider import HOSTING_PROVIDER


# CONFIG_MODEL = t.Dict({
#     t.Key("kind"): t.Regexp(r"^ctf$"),
#     t.Key("name"): t.String(),
#     t.Key("challenges"): t.List(t.String()),
#     t.Key("deployments", default=[]): t.List(t.Dict({
#         t.Key("environment"): t.Regexp(enum_to_regex(HOSTING_ENVIRONMENT)),
#         t.Key("provider"): t.Regexp(enum_to_regex(HOSTING_PROVIDER)),
#         t.Key("cluster"): t.Dict({
#             t.Key("machine_type"): t.String(),
#             t.Key("node_count"): t.Int(),
#         }),
#     })),
# })


@dataclass
class CtfConfig():

    @dataclass
    class DeploymentConfig:

        @dataclass
        class ClusterConfig:
            machine_type: str = 'n1-standard-4'
            node_count: int = 1

        environment: HOSTING_ENVIRONMENT = HOSTING_ENVIRONMENT.TESTING
        provider: HOSTING_PROVIDER = HOSTING_PROVIDER.GCP
        cluster: ClusterConfig = ClusterConfig()

    kind: str
    name: str
    challenge: List[str] = []
    deployments: List[DeploymentConfig] = []

    def getSlug(self) -> str:
        slugify(self.name)



        # try:
        #     return trafaret_config.read_and_validate(config_file, CONFIG_MODEL)

        # except trafaret_config.ConfigError as e:
        #     self.fail("\n".join(str(err) for err in e.errors))
