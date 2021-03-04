from os import path
from unittest import TestCase, main

from click.testing import CliRunner

from ctfkit.cli import root_cli


class TestCliCtf(TestCase):
    runner = CliRunner()

    VALID_CONFIG = """kind: ctf
kind: ctf
name: fakectf
deployments:
    -   environment: testing
        provider: gcp
        gcp:
            project: fakectf
            region: europe-west1
            zone: europe-west1-b
"""

    GCP_CREDENTIALS = """{
    "type": "service_account",
    "project_id": "",
    "private_key_id": "",
    "private_key": "-----BEGIN PRIVATE KEY----------END PRIVATE KEY-----\\n",
    "client_email": "",
    "client_id": "",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": ""
}"""

    # def test_plan(self):
    #     with self.runner.isolated_filesystem():
    #         with open('ctf.yaml', 'w') as config:
    #             config.write(self.VALID_CONFIG)
    #             config.close()

    #         with open('credentials.json', 'w') as credentials:
    #             credentials.write(self.GCP_CREDENTIALS)

    #         result = self.runner.invoke(root_cli, ['ctf', 'plan', 'testing'])
    #         self.assertEqual(result.exit_code, 0)

    #         self.assertTrue(path.exists('.tfout'))

if __name__ == '__main__':
    main()
