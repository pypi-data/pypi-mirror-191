import click
from omega.cli.convert import convert


@click.group(
    help="Example: snypr-cli convert -m mapping.yml rules.yml",
)
def cli():
    pass


def main():
    cli.add_command(convert)
    cli()
