from uuid import UUID

import typer

cli = typer.Typer()


@cli.command()
def get(match_report_id: UUID):
    pass


if __name__ == "__main__":
    cli()
