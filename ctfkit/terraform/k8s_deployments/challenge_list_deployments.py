from typing import List, Optional

from constructs import Construct
from cdktf import Resource

from ctfkit.models.challenge_config import ChallengeConfig
from .challenge_deployment import K8sChallengeDeployment


class K8sChallengeListDeployments(Resource):
    """
    A kubernetes resource which deploy specified challenges to a specified namespace
    """

    def __init__(
            self,
            scope: Construct,
            name: str,
            challenges: List[ChallengeConfig],
            namespace: Optional[str] = 'default') -> None:
        super().__init__(scope, name)

        for challenge_config in challenges:
            K8sChallengeDeployment(self, challenge_config, namespace)
