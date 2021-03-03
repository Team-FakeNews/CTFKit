import unittest
from os.path import join
from ctfkit.challenge import Challenge
from ctfkit.models import challenge_config
from ctfkit.utility import ConfigLoader


class TestCreateChallengeFunctions(unittest.TestCase):

    challenge_config_valid = join('example', 'challs', '01-test',
                                  'challenge.yml')
    challenge_valid = Challenge(config="""{'name':'chall',
    'description':'blablabla','points':10,'category':'pwn',
    'author':'0xLaPoutre','files':['chall.jpg'],
    'container':[{'proto':'tcp','port':1337},{'proto':'udp','port':42}]""")

    # Check that a Challenge object is well formed using a valid YAML challenge
    # config file
    def test_challenge_from_yaml(self):
        self.assertTrue(
            type(Challenge.from_yaml(self.challenge_config_valid)) ==
            type(self.challenge_valid))


if __name__ == '__main__':
    unittest.main()
