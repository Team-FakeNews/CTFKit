import unittest
from os import getcwd, system
from os.path import isdir, join

from click.testing import CliRunner

from ctfkit.cli import root_cli


class TestCreateCTF(unittest.TestCase):
    """This class will pass the unittests once ctf.yaml will be implemented
    For the moment the ctfkit/cli/ctf.py requires a ctf config file (default as ctf.yaml)
    """
    runner = CliRunner()

    ctf_name_invalid = "tést ÇétéÈfe"
    ctf_name_valid = "test-ctf"
    path = getcwd()

    # Check that a CTF is not created if the name is not valid, and vice versa
    def test_new_ctf(self):
        # Check for invalid name
        result = self.runner.invoke(
            root_cli, ["ctf", "init", "-p", "gcp", "-n", self.ctf_name_invalid])
        self.assertFalse(isdir(join(self.path, self.ctf_name_invalid)))

        # Check for valid name
        result = self.runner.invoke(
            root_cli, ["ctf", "init", "-p", "gcp", "-n", self.ctf_name_valid])
        self.assertTrue(isdir(join(self.path, self.ctf_name_valid)))


if __name__ == '__main__':
    unittest.main()
