import click
import validators

from . import create_challenge


def check_challenge_name(name: str) -> bool:
    """Check if a given name is valid for a new challenge

    :param name: The name to check
    :type name: str
    :return: True if the given name is valid, False else
    :rtype: bool
    """
    if not validators.slug(name):
        print(f"{name} is not a valid name. You must supply a valid name for a new challenge (must be a slug format)")
        return False
    else:
        return True


def check_challenge_url(url: str) -> bool:
    """Check if a given URL is valid for a challenge import

    :param url: The URL to check
    :type url: str
    :return: True if the given URL is valid, False else
    :rtype: bool
    """
    if not validators.url(url):
        print(f"{url} is not a valid URL. You must supply a valid URL for a challenge import (http:// or https://)")
        return False
    else:
        return True


@click.group()
def cli() -> None:
    pass


@cli.command('new')
@click.argument('challenge_name', nargs=1)
def new(challenge_name: str) -> None:
    """<challenge_name>: Creates a CTF Kit challenge repo for a new challenge

    :param challenge_name: The name of the challenge to create
    :type challenge_name: str
    """
    if check_challenge_name(challenge_name):
        create_challenge.new_challenge(challenge_name)


@cli.command('add')
@click.argument('challenge_url', nargs=1)
def add(challenge_url: str) -> None:
    """<challenge_url>: Import a challenge with its URL (must be a GIT repo)

    :param challenge_url: The URL of the challenge to import
    :type challenge_url: str
    """
    if check_challenge_url(challenge_url):
        create_challenge.add_challenge(challenge_url)
