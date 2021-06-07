# Installation

## Requirements

- Python >= 3.8
- NodeJS >= LTS
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- [gcloud CLI](https://cloud.google.com/sdk/docs/install)

!!! info
    NodeJS, Terraform and GCloud are only required for infrastructure features.

    If you do not intend to use deployment features, you can skip them.

## Download

While CTFKit is in beta, no package will be distributed on pip.
You need to clone from source sources and install the package yourself.

You can get the latest version from the official repository : `git clone https://git.fakenews.sh/ctfkit/ctfkit.git`

## Installation

Once the repository is clone you can install the package globaly with :
```
pip install .
```

Alternatively, you can use CTFKit without any installation by calling the binary :
```bash
python3 
```

## Checks

If the package has correctly been installed, you should be able to run directly :
```bash
> ctfkit
Usage: ctfkit [OPTIONS] COMMAND [ARGS]...

  Main cli which contains all sub-commands It doesn't do anything but showing
  help to the user

Options:
  --help  Show this message and exit.

Commands:
  challenge
  ctf        Root group for the ctf command
```

If your terminal cannot find any executable matching `ctfkit`, maybe your pip installation folder has not been
added to PATH. In this case, you can always run ctfkit using `python3 -m ctfkit`.

You can refer to the official python documentation for adding pip packages to your PATH.

## GCloud configuration

If your aim is to deploy a CTF to gcloud, you need a proper installation of.

