import click
from sigma.backends.base import BackendOptions
from sigma.parser.collection import SigmaCollectionParser

from omega.cli.spotter import Spotter
from omega.cli.configuration import Configuration


@click.command()
@click.option(
    "--mapping", "-m",
    help="Omega mapping file",
    required=True,
)
@click.argument(
    "input",
    #type=click.Path(exists=True, path_type=pathlib.Path),
)
def convert(input, mapping):
    """
    Convert Omega rules into queries. INPUT can be multiple files or directories. This command automatically recurses
    into directories and converts all files matching the pattern in --file-pattern.
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
