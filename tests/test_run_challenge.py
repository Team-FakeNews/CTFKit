import unittest
import os
from ctfkit.cli.challenge import *
from click.testing import CliRunner
from ctfkit.cli import root_cli


# class TestRunChallengeFunctions(unittest.TestCase):
#     runner = CliRunner()
#     print(os.getcwd())
#     challenge_valid = '01-test'
#     challenge_invalid = 'XX-test'
#     os.chdir(r"./example/challs")

#     def test_run_challenge(self):
#         result = self.runner.invoke(root_cli, ['challenge', 'run', self.challenge_valid])
#         self.assertEqual(result.exit_code, 0)

#         result = self.runner.invoke(root_cli, ['challenge', 'run', self.challenge_invalid])
#         self.assertEqual(result.exit_code, 1)

#     def test_stop_challenge(self):
#         result = self.runner.invoke(root_cli, ['challenge', 'stop', self.challenge_valid])
#         self.assertEqual(result.exit_code, 0)

#         result = self.runner.invoke(root_cli, ['challenge', 'stop', self.challenge_invalid])
#         self.assertEqual(result.exit_code, 1)


# if __name__ == '__main__':
#     unittest.main()
