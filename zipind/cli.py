"""Console script for zipind."""
import sys

import click

from . import zipind


@click.group(invoke_without_command=True)
@click.pass_context
def cli_group(ctx):
    if ctx.invoked_subcommand is None:
        main()
        pass


@click.option("-a", "arg", type=click.INT)
@cli_group.command()
def rel(arg):

    click.echo(f"funcao rel ativada, com arg: {str(arg)}")
    # click.echo("funcao rel ativada, com arg:", str(arg))


def main(args=None):
    """Console script for zipind."""
    click.echo("modo chatbot")
    zipind.main()
    return 0


if __name__ == "__main__":
    # sys.exit(main())  # pragma: no cover
    sys.exit(cli_group())  # pragma: no cover
