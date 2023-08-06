from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import defaults as _defaults


def get_sqlalchemy_url(
    scheme: str = _defaults.HITFACTORPY_DB_CONNECTION_SCHEME,
    username: str = _defaults.HITFACTORPY_DB_USERNAME,
    password: str = _defaults.HITFACTORPY_DB_PASSWORD,
    host: str = _defaults.HITFACTORPY_DB_HOST,
    port: int = _defaults.HITFACTORPY_DB_PORT,
    database: str = _defaults.HITFACTORPY_DB_DATABASE_NAME,
):
    return URL.create(  # type: ignore
        scheme,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
    )


def make_async_session(sqlalchemy_url: str):
    engine = create_async_engine(sqlalchemy_url)
    return sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


def make_sync_session(sqlalchemy_url: str):
    engine = create_engine(sqlalchemy_url)
    return sessionmaker(bind=engine)
