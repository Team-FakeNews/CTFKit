import click

@click.group()
def cli():
    pass

@cli.command('init')
def init():
    pass
