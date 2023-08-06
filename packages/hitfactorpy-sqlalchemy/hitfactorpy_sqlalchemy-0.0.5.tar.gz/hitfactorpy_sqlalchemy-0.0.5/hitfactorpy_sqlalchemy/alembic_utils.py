from pathlib import Path

from alembic.config import Config as AlembicConfig

from .defaults import HITFACTORPY_DB_ALEMBIC_DIR
from .session import get_sqlalchemy_url


def HitfactorpyAlembicConfig(
    script_location: str | Path = HITFACTORPY_DB_ALEMBIC_DIR, sqlalchemy_url: str = get_sqlalchemy_url()
) -> AlembicConfig:
    alembic_cfg = AlembicConfig()
    alembic_cfg.set_main_option("script_location", str(script_location))
    alembic_cfg.set_main_option("sqlalchemy.url", sqlalchemy_url)
    return alembic_cfg
