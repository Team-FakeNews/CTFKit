from os import path
from unittest import TestCase

from click.testing import CliRunner

from ctfkit.cli import root_cli



class TestCliCtf(TestCase):
    runner = CliRunner()

    VALID_CONFIG="""kind: ctf
name: fakectf
challenges:
    - ./challs/01-test
deployments:
    - environment: testing
      provider: gcp
"""

    def test_plan(self):
        with self.runner.isolated_filesystem():
            with open('ctf.config.yaml', 'w') as config:
                config.write(self.VALID_CONFIG)
                config.close()

            result = self.runner.invoke(root_cli, ['ctf', 'plan', 'testing'])
            self.assertEqual(result.exit_code, 0)

            self.assertTrue(path.exists('.tfout'))

