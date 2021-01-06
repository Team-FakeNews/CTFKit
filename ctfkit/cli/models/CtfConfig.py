import click
from click.core import Context, Parameter
from click.types import Path
import trafaret as t
import trafaret_config
from typing import Optional

from ctfkit.cli.models.HostingProvider import HOSTING_PROVIDER
from ctfkit.cli.models.HostingEnvironment import HOSTING_ENVIRONMENT
from ctfkit.utility import enum_to_regex

CONFIG_MODEL = t.Dict({
    t.Key("kind"): t.Regexp(r"^ctf$"),
    t.Key("name"): t.String(),
    t.Key("challenges"): t.List(t.String()),
    t.Key("deployments", default=[]): t.List(t.Dict({
        # t.Key("environment"): t.Enum(HOSTING_ENVIRONMENT),
        t.Key("environment"): t.Regexp(enum_to_regex(HOSTING_ENVIRONMENT)),
        t.Key("provider"): t.Regexp(enum_to_regex(HOSTING_PROVIDER)),
    }))
})


class CtfConfig(click.Path):

    def __init__(self) -> None:
        super().__init__(exists=True, file_okay=True, dir_okay=False, readable=True)

    def convert(self, value: str, param: Optional[Parameter], ctx: Optional[Context]) -> Path:
        config_file = super().convert(value, param, ctx)

        try:
            return trafaret_config.read_and_validate(config_file, CONFIG_MODEL)

        except trafaret_config.ConfigError as e:
            self.fail("\n".join(str(err) for err in e.errors))
