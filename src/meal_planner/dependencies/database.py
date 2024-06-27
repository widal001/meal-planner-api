# pylint: disable=invalid-name
"""Manage connection to the database using a SQLAlchemy session factory."""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from meal_planner.config import settings


def create_session_factory() -> sessionmaker:  # pragma: no cover
    """Create a sessionmaker with database connection details."""
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:  # pragma: no cover
    """
    Yield a connection to the database to manage transactions.

    Yields
    ------
    Session
        A SQLAlchemy session that manages a connection to the database

    """
    SessionFactory = create_session_factory()  # noqa: N806

    try:
        db = SessionFactory()
        yield db
    finally:
        db.close()
