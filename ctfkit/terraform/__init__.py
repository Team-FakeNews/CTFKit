from constructs import Construct
from cdktf import TerraformStack


class CtfStack(TerraformStack):
    """
    Root terraform stack which should contains every ressources
    needed to build up an infrastructure
    """
    def __init__(self, scope: Construct, name: str) -> None:
        super().__init__(scope, name)
