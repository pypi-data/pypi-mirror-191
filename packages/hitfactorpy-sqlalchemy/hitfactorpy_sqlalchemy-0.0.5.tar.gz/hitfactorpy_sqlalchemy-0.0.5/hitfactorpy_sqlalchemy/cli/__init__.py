import typer

from .import_ import cli as import_cli
from .migrate import cli as migrate_cli
from .model import cli as model_cli

CLI_NAME = "hitfactorpy_sqlalchemy"


cli = typer.Typer()


def version_callback(value: bool):
    from .. import __version__ as pkg_version

    if value:
        typer.echo(pkg_version)
        raise typer.Exit()


@cli.callback()
def main(
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True, help="Show program version and exit"
    ),
):
    pass


cli.add_typer(import_cli, name="import", help="import data")
cli.add_typer(migrate_cli, name="migrate", help="manage db migrations")
cli.add_typer(model_cli, name="model", help="manage models directly")


if __name__ == "__main__":
    cli()
