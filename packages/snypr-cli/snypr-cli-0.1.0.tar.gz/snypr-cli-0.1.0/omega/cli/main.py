import click
from omega.cli.convert import convert


@click.group()
def cli():
    pass


def main():
    cli.add_command(convert)
    cli()
