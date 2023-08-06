import click
from sigma.backends.base import BackendOptions
from sigma.parser.collection import SigmaCollectionParser

from omega.cli.spotter import Spotter
from omega.cli.configuration import Configuration


@click.command(
    "convert",
    help="Convert Sigma rules into queries.",
)
@click.option(
    "--mapping", "-m",
    help="Snyper mapping file",
    required=True,
)
@click.argument(
    "input",
    required=True,
)
def convert(input, mapping):
    """
    Convert Sigma rules into queries.
    """

    query = ""
    try:
        with open(mapping, 'r') as stream:
            sigmaconfigs = Configuration(configyaml=stream)
        spotter_backend = Spotter(sigmaconfigs, BackendOptions(None, None))
        with open(input, 'r') as rule:
            parser = SigmaCollectionParser(rule, sigmaconfigs, None)
            results = parser.generate(spotter_backend)
        for result in results:
            query = query + result
        click.echo(f"\n\nindex = activity AND {query} \n\n")
    except FileNotFoundError as e:
        click.echo(f"{e}")
