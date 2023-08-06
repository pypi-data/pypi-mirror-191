import typer

from .match_report import cli as match_report_cli

cli = typer.Typer()
cli.add_typer(match_report_cli, name="match-report", help="manage match-report models")


if __name__ == "__main__":
    cli()
