import hashlib
import sys
import uuid
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict

import typer
from hitfactorpy.decimal_ import D4
from hitfactorpy.parsers.match_report.pandas import parse_match_report
from rich import print
from rich.console import Console
from sqlalchemy.engine.url import URL

from .. import defaults as _defaults
from .. import env as _env

cli = typer.Typer()
stderr = Console(stderr=True)


@dataclass(frozen=True)
class CtxDbConnection:
    scheme: str
    username: str
    password: str
    host: str
    port: int
    database: str


@dataclass(frozen=True)
class CtxObj:
    db_connection: CtxDbConnection
    sqlalchemy_url: str


@cli.callback()
def inject_shared_options(
    ctx: typer.Context,
    username: str = typer.Option(
        _defaults.HITFACTORPY_DB_USERNAME, help="Username for DB connection", envvar=_env.HITFACTORPY_DB_USERNAME
    ),
    password: str = typer.Option(
        _defaults.HITFACTORPY_DB_PASSWORD, help="Password for DB connection", envvar=_env.HITFACTORPY_DB_USERNAME
    ),
    host: str = typer.Option(_defaults.HITFACTORPY_DB_HOST, help="Database host", envvar=_env.HITFACTORPY_DB_HOST),
    port: int = typer.Option(_defaults.HITFACTORPY_DB_PORT, help="Database port", envvar=_env.HITFACTORPY_DB_PORT),
    database: str = typer.Option(
        _defaults.HITFACTORPY_DB_DATABASE_NAME, help="Database name", envvar=_env.HITFACTORPY_DB_DATABASE_NAME
    ),
    scheme: str = typer.Option(
        _defaults.HITFACTORPY_DB_CONNECTION_SCHEME,
        help="SQLAlchemy database connection protocol",
        envvar=_env.HITFACTORPY_DB_CONNECTION_SCHEME,
    ),
):
    db_conn = CtxDbConnection(
        scheme=scheme,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
    )
    ctx.obj = CtxObj(
        db_connection=db_conn,
        sqlalchemy_url=str(
            URL.create(  # type: ignore
                db_conn.scheme,
                username=db_conn.username,
                password=db_conn.password,
                host=db_conn.host,
                port=db_conn.port,
                database=db_conn.database,
            )
        ),
    )


@cli.command()
def debug(ctx: typer.Context):
    """open a debugger with an active sqlalchemy session"""
    from hitfactorpy_sqlalchemy.session import make_sync_session

    config: CtxObj = ctx.obj
    Session = make_sync_session(config.sqlalchemy_url)

    with Session() as session:
        import sqlalchemy as sa

        from hitfactorpy_sqlalchemy.orm.models import MatchReport, MatchReportStageScore

        stmt = sa.select(MatchReport)
        result = session.execute(stmt)
        match_report = result.fetchone()[0]
        print(match_report.name)

        num_stage_scores = session.query(sa.func.count(MatchReportStageScore.id)).scalar()
        print(f"total scores: {num_stage_scores}")

        stmt4 = sa.select(MatchReportStageScore).where(
            MatchReportStageScore.calculated_hit_factor == MatchReportStageScore.hit_factor
        )
        result4 = session.execute(stmt4)
        scores4 = [r[0] for r in result4.fetchall()]
        print(f"scores where hit_factor == calculated_hit_factor: {len(scores4)}")

        stmt3 = sa.select(MatchReportStageScore).where(
            MatchReportStageScore.calculated_hit_factor != MatchReportStageScore.hit_factor
        )
        result3 = session.execute(stmt3)
        scores3 = [r[0] for r in result3.fetchall()]
        print(f"scores where hit_factor != calculated_hit_factor (SQL): {len(scores3)}")
        score_mismatches_python = [s for s in scores3 if s.hit_factor != s.calculated_hit_factor]
        smp = score_mismatches_python
        print(f"scores where hit_factor != calculated_hit_factor (PYTHON): {len(smp)}")

        breakpoint()

        session.close()


@cli.command()
def match_report(
    ctx: typer.Context,
    file: typer.FileText = typer.Argument(sys.stdin, help="Report file in raw (.txt) format"),
):
    """import a match report"""
    from hitfactorpy_sqlalchemy.orm.models import (
        MatchReport,
        MatchReportCompetitor,
        MatchReportStage,
        MatchReportStageScore,
    )
    from hitfactorpy_sqlalchemy.session import make_sync_session

    config: CtxObj = ctx.obj

    file_text = "\n".join(file.readlines())
    file_hash = hashlib.md5(file_text.encode()).hexdigest()

    Session = make_sync_session(config.sqlalchemy_url)

    with Session() as session:
        # Check if match has already been imported
        existing = session.query(MatchReport).where(MatchReport.report_hash == uuid.UUID(file_hash)).count()
        if existing:
            stderr.print("report has already been imported")
            session.rollback()
            session.close()
            raise typer.Exit(1)

        parsed_match_report = parse_match_report(file_text)

        match_report = MatchReport(  # type: ignore
            name=parsed_match_report.name,
            date=parsed_match_report.date,
            match_level=parsed_match_report.match_level,
            report_hash=file_hash,
        )
        session.add(match_report)

        competitors: Dict[int, MatchReportCompetitor] = {}
        if parsed_match_report.competitors:
            for c in parsed_match_report.competitors:
                competitor_model = MatchReportCompetitor(  # type: ignore
                    member_number=c.member_number,
                    first_name=c.first_name,
                    last_name=c.last_name,
                    division=c.division,
                    power_factor=c.power_factor,
                    classification=c.classification,
                    dq=c.dq,
                    reentry=c.reentry,
                    match=match_report,
                )
                session.add(competitor_model)
                competitors[c.internal_id] = competitor_model

        stages: Dict[int, MatchReportStage] = {}
        if parsed_match_report.stages:
            for s in parsed_match_report.stages:
                stage_model = MatchReportStage(  # type: ignore
                    name=s.name,
                    min_rounds=s.min_rounds,
                    max_points=s.max_points,
                    classifier=s.classifier,
                    classifier_number=s.classifier_number,
                    scoring_type=s.scoring_type,
                    stage_number=s.internal_id,
                    match=match_report,
                )
                session.add(stage_model)
                stages[s.internal_id] = stage_model

        if parsed_match_report.stage_scores:
            for sc in parsed_match_report.stage_scores:
                stage_score_model = MatchReportStageScore(  # type: ignore
                    match=match_report,
                    competitor=competitors[sc.competitor_id or -1],
                    stage=stages[sc.stage_id or -1],
                    dq=sc.dq,
                    dnf=sc.dnf,
                    a=sc.a,
                    b=sc.b,
                    c=sc.c,
                    d=sc.d,
                    m=sc.m,
                    npm=sc.npm,
                    ns=sc.ns,
                    procedural=sc.procedural,
                    late_shot=sc.late_shot,
                    extra_shot=sc.extra_shot,
                    extra_hit=sc.extra_hit,
                    other_penalty=sc.other_penalty,
                    t1=sc.t1,
                    t2=sc.t2,
                    t3=sc.t3,
                    t4=sc.t4,
                    t5=sc.t5,
                    time=sc.time,
                    raw_points=sc.raw_points,
                    penalty_points=sc.penalty_points,
                    total_points=sc.total_points,
                    hit_factor=sc.hit_factor,
                    stage_points=sc.stage_points,
                    stage_place=sc.stage_place,
                    stage_power_factor=sc.stage_power_factor,
                )
                session.add(stage_score_model)
                if stage_score_model.calculated_hit_factor != D4(stage_score_model.hit_factor):
                    stderr.print(
                        f"found score where hf({stage_score_model.hit_factor}) != calculated_hf({stage_score_model.calculated_hit_factor})"
                    )
                    session.rollback()
                    session.close()
                    raise typer.Exit(1)

        typer.echo("Committing changes...")
        session.commit()
        session.close()


if __name__ == "__main__":
    cli()
