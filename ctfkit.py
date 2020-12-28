#!/usr/bin/env python3
# coding: utf-8

import argparse
import validators

from ctfkit import *


def check_challenge_name(name):
    """Check if a given name is valid for a new challenge

    :param name: The name to check
    :type name: str
    :return: True if the given name is valid, False else
    :rtype: bool
    """
    if not validators.slug(name):
        print("You must supply a valid name for a new challenge (must be a slug format)")
        return False
    else:
        return True


def check_challenge_url(url):
    """Check if a given URL is valid for a challenge import

    :param url: The URL to check
    :type url: str
    :return: True if the given URL is valid, False else
    :rtype: bool
    """
    if not validators.url(url):
        print("You must supply a valid URL for a challenge import (http:// or https://)")
        return False
    else:
        return True


def new_challenge(name):
    """Create a new challenge sub-module for CTF Kit

    :param name: The name of the challenge
    :type name: str
    """
    print(f"New challenge {name}")


def add_challenge(url):
    """Import a challenge with its URL

    :param url: The URL of the challenge (CTF Kit sub-module)
    :type url: str
    """
    print(f"Import challenge at {url}")


def main():
    """The main function of the programm, parses arguments to correctly use the CTF Kit module.
    """
    # We set up the parser
    parser = argparse.ArgumentParser(
        description="Create or import CTF Kit-compatible challenges")
    # We set up the arguments
    """Actual arguments we use
	- ctfkit.py new <challenge_name>
	- ctfkit.py add <challenge_url>
	"""
    parser.add_argument("action", type=str, help="Must be one of: new, add.")
    parser.add_argument("challenge", type=str,
                        help="Challenge's name for a new challenge, or challenge's URL for importing")

    # We parse the arguments in order to call one function depending on the given arguments
    args = parser.parse_args()

    if args.action == "new":
        # User wants to create a new challenge
        print("Creation of a new challenge...")
        # Check if challenge name has been supplied
        if args.challenge:
            # Check if name is valid
            if check_challenge_name(args.challenge):
                new_challenge(args.challenge)
            else:
                print("Supplied name is not valid")
        else:
            print("You must provide a name for the challenge")
    elif args.action == "add":
        # User wants to import a challenge
        print("Import of a challenge...")
        # Check if challenge url has been supplied
        if args.challenge:
            # Check if challenge URL is valid
            if check_challenge_url(args.challenge):
                add_challenge(args.challenge)
            else:
                print("Suplied URL is not valid")
        else:
            print("You must supply an URL for the challenge")
    else:
        print("First argument must be one of: new, add")


if __name__ == "__main__":
    main()
