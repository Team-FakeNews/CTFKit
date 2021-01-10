from constructs import Construct
from cdktf import TerraformStack


class CtfStack(TerraformStack):

    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)
