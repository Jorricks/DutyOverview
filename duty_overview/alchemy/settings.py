import logging
import os
from typing import Any, Callable

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy.orm.session import Session as SASession

log = logging.getLogger(__name__)
SQL_ALCHEMY_CONN: str = os.environ.get("SQL_ALCHEMY_CONNECTION", "")
engine: Engine
Session: Callable[..., SASession]
Base: Any = declarative_base()


def get_engine() -> Engine:
    return engine


def prepare_engine_args():
    """Prepare SQLAlchemy engine args for a postgres connection"""
    return {
        "executemany_mode": "values",
        "executemany_values_page_size": 10000,
        "executemany_batch_page_size": 2000,
        "pool_size": 5,
        "pool_recycle": 1800,
        "pool_pre_ping": True,
        "max_overflow": 10,
        "encoding": "utf-8",
    }


def dispose_orm():
    """Properly close pooled database connections"""
    log.debug("Disposing DB connection pool (PID %s)", os.getpid())
    global engine
    global Session

    if Session:
        Session.remove()
        Session = None
    if engine:
        engine.dispose()
        engine = None


def reconfigure_orm():
    """Properly close database connections and re-configure ORM"""
    dispose_orm()
    configure_orm()


def configure_orm():
    """Configure ORM using SQLAlchemy"""
    log.debug("Setting up DB connection pool (PID %s)", os.getpid())
    global engine
    global Session
    engine_args = prepare_engine_args()
    engine = create_engine(SQL_ALCHEMY_CONN, connect_args={}, **engine_args)
    Session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            expire_on_commit=False,
        )
    )
