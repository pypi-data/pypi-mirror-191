from os import path
from pathlib import Path

HITFACTORPY_MODULE_PATH = Path(path.dirname(path.abspath(__file__)))
HITFACTORPY_DB_ALEMBIC_DIR = HITFACTORPY_MODULE_PATH / "migrations"
HITFACTORPY_DB_USERNAME = "postgres"
HITFACTORPY_DB_PASSWORD = "postgres"
HITFACTORPY_DB_HOST = "localhost"
HITFACTORPY_DB_PORT = 5432
HITFACTORPY_DB_DATABASE_NAME = "hitfactorpy"
HITFACTORPY_DB_CONNECTION_SCHEME = "postgresql+psycopg2"
