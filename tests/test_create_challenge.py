import unittest
import os

from ctfkit.challenge import Challenge
from ctfkit.cli.challenge import *
from ctfkit.models import challenge_config
from ctfkit.utility import ConfigLoader


class TestCreateChallengeFunctions(unittest.TestCase):

    challenge_name_valid = 'my-new-challenge'
    challenge_name_invalid = 'mÿ néw CHallenge'
    challenge_url_valid = 'http://my-git.com/my-ctfkit-challenge'
    challenge_url_invalid = '///my-git/my-ctfkit-challenge'
    challenge_config_valid = os.path.join('example', 'challs', '01-test',
                                          'challenge.yml')
    challenge_valid = Challenge(config="""{'name':'chall',
    'description':'blablabla','points':10,'category':'pwn',
    'author':'0xLaPoutre','files':['chall.jpg'],
    'container':[{'proto':'tcp','port':1337},{'proto':'udp','port':71337}]""")

    # Check that a challenge is not created if the name is not valid, and vice
    # versa
    def test_new_challenge(self):
        self.assertTrue(check_challenge_name(self.challenge_name_valid))
        self.assertFalse(check_challenge_name(self.challenge_name_invalid))

    # Check that a challenge is not imported if the url is not valid and vice
    # versa
    def test_add_challenge(self):
        self.assertTrue(check_challenge_url(self.challenge_url_valid))
        self.assertFalse(check_challenge_url(self.challenge_url_invalid))

    # Check that a Challenge object is well formed using a valid YAML challenge
    # config file
    def test_challenge_from_yaml(self):
        self.assertTrue(
            type(Challenge.from_yaml(self.challenge_config_valid)) ==
            type(self.challenge_valid))


if __name__ == '__main__':
    unittest.main()
