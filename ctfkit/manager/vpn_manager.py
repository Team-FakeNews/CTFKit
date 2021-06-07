from os.path import join
from typing import Dict, List
from nacl.public import PrivateKey, PublicKey
from base64 import b64decode, b64encode

from ctfkit.utility import mkdir
from ctfkit.models.team import Team

class VPNManager:

    @staticmethod
    def generate_clients_private(teams: List[Team]):
        mkdir('vpn_configs')
        for team in teams:
            team_folder = join('vpn_configs', team.name)
            mkdir(team_folder)

            # Generate server private key
            private_key_path = join(team_folder, 'private_key')
            try:
                with open(private_key_path, 'r') as file_handler:
                    private_key = PrivateKey(b64decode(file_handler.read()))
            except FileNotFoundError:
                with open(private_key_path, 'w') as file_handler:
                    private_key = PrivateKey.generate()
                    file_handler.write(b64encode(bytes(private_key)).decode())

            team.private_key = private_key

            for member in team.members:
                member_folder = join(team_folder, member.name)
                mkdir(member_folder)

                private_key_path = join(member_folder, 'private_key')
                try:
                    with open(private_key_path, 'r') as file_handler:
                        private_key = PrivateKey(b64decode(file_handler.read()))
                except FileNotFoundError:
                    with open(private_key_path, 'w') as file_handler:
                        private_key = PrivateKey.generate()
                        file_handler.write(b64encode(bytes(private_key)).decode())

                member.private_key = private_key

    @staticmethod
    def generate_clients_config(
            teams: List[Team],
            servers_endpoints: Dict[str, str],
            services_cidr: str):
        for team in teams:
            for index, member in enumerate(team.members):

                with open(join('vpn_configs', team.name, member.name, 'ctf.conf'), 'w') as file_handler:
                    file_handler.write(f"""[Interface]
Address = 10.8.8.{index+2}/32
PrivateKey = {b64encode(bytes(member.private_key)).decode()}
DNS = 10.8.8.1

# ==== Server configuration ====

[Peer]
PublicKey = {b64encode(bytes(team.private_key.public_key)).decode()}
Endpoint = {servers_endpoints[team.name]}
AllowedIPs = 10.8.8.1/32, {services_cidr}
PersistentKeepalive = 25
""")
