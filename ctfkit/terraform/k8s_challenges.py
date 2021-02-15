from typing import List

from constructs import Construct
from cdktf import Resource

from ctfkit.models.challenge_config import ChallengeConfig
from .challenge_deployment import ChallengeDeployment


class K8sChallenges(Resource):
    def __init__(self, scope: Construct, name: str, challenges: List[ChallengeConfig]) -> None:
        super().__init__(scope, name)

        for challenge_config in challenges:
            ChallengeDeployment(self, challenge_config)
