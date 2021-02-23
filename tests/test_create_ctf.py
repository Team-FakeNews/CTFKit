import unittest
from os import getcwd, system
from os.path import isdir, join

from ctfkit.cli.ctf import *


class TestCreateCTF(unittest.TestCase):
    """This class will pass the unittests once ctf.yaml will be implemented
    For the moment the ctfkit/cli/ctf.py requires a ctf config file (default as ctf.yaml)
    """

    ctf_name_valid = "test-ctf"
    ctf_name_invalid = "tést ÇétéÈfe"
    path = getcwd()

    # Check that a CTF is not created if the name is not valid, and vice versa
    def test_new_ctf(self):
        # Check for invalid name
        system(f"ctfkit ctf init -p gcp -n {self.ctf_name_invalid}")
        self.assertFalse(isdir(join(self.path, self.ctf_name_invalid)))

        # Check for valid name
        system(f"ctfkit ctf init -p gcp -n {self.ctf_name_valid}")
        self.assertTrue(isdir(join(self.path, self.ctf_name_valid)))


if __name__ == '__main__':
    unittest.main()
