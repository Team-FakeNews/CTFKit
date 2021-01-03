import click

@click.group('challenge')
def cli():
    pass

@cli.command('init')
def init():
    pass
