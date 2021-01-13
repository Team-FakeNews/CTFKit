from time import sleep
import logging
from tempfile import NamedTemporaryFile
from shutil import rmtree
from typing import IO
from unittest import main, TestCase

from click.exceptions import BadParameter
from marshmallow import ValidationError
from marshmallow_dataclass import dataclass
from ctfkit.utility import ConfigLoader

@dataclass
class ExampleDataclass:
    a: str
    b: int


class TestConfigLoader(TestCase):

    def create_temp(self, content: str) -> str:
        config_file = NamedTemporaryFile()
        config_file.write(bytes(content, 'utf8'))
        config_file.flush()

        return config_file

    def test_nominal(self):
        with self.create_temp('a: "str_value"\nb: 10\n') as config_file:
            instance: ExampleDataclass = ConfigLoader(ExampleDataclass).convert(config_file.name)

            self.assertIsInstance(instance, ExampleDataclass)
            self.assertEqual(instance.a, "str_value")
            self.assertEqual(instance.b, 10)

    def test_extraneous_member(self):
        with self.create_temp('a: "str_value"\nb: 10\nc: "hihi"\n') as config_file:
            with self.assertRaises(ValidationError):
                ConfigLoader(ExampleDataclass).convert(config_file.name)

    def test_missing_member(self):
        with self.create_temp('a: "str_value"\nb: 10\nc: "hihi"\n') as config_file:
            with self.assertRaises(ValidationError):
                ConfigLoader(ExampleDataclass).convert(config_file.name)

    def test_not_dataclass(self) -> None:
        class NotADataclass:
            a: str
            b: int

        with self.assertRaises(ValueError):
            ConfigLoader(NotADataclass).convert(self.config_file.name)

    def test_file_not_found(self) -> None:
        with self.assertRaises(BadParameter):
            ConfigLoader(ExampleDataclass).convert('plop.txt')


if __name__ == '__main__':
    main
