# pylint: disable=no-self-argument
"""Create base models that other models can inherit from."""

from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from sqlalchemy.sql import functions


class UUIDAuditBase(DeclarativeBase):
    """Base db model that includes id, created_at, and update_at."""

    id: Mapped[UUID] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=functions.now(),
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=functions.now(),
        onupdate=functions.now(),
    )
