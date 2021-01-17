import unittest
import os
from ctfkit.cli.challenge import *

class TestRunChallengeFunctions(unittest.TestCase):
    challenge_valid = 'chall01'
    challenge_invalid = 'chall02'

    # Run a challenge using his name (the name of the challenge is a directory located at the root of ctfkit)
    def test_run_challenge(self):
        self.assertTrue(run(self.challenge_valid))
        self.assertFalse(run(self.challenge_invalid))


    def test_stop_challenge(self):
        self.assertTrue(stop(self.challenge_valid))
        self.assertFalse(stop(self.challenge_invalid))


if __name__ == '__main__':
    unittest.main()
