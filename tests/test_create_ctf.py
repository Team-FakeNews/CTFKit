import unittest
from os import system
from os.path import isdir, isfile, join

from ctfkit.cli.ctf import *
from ctfkit.utility import get_current_path


class TestCreateCTF(unittest.TestCase):
    
    ctf_name_valid = "test-ctf"
    ctf_name_invalid = "tést ÇétéÈfe"
    path = get_current_path()

    # Check that a CTF is not created if the name is not valid, and vice versa
    def test_new_ctf(self):
        # Check for invalid name
        system(f"ctfkit ctf init -n {ctf_name_invalid}")
        self.assertFalse(isdir(join(path, ctf_name_invalid)))

        # Check for valid name
        system(f"ctfkit ctf init -n {ctf_name_valid}")
        self.assertTrue(isdir(join(path, ctf_name_valid)))


if __name__ == '__main__':
    unittest.main()
