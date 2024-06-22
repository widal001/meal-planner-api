"""Manage shared CRUD logic."""

from typing import Generic, Sequence, Type, TypeVar
from uuid import UUID, uuid4

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.orm import Session

from meal_planner.models.base import UUIDAuditBase

ModelTypeT = TypeVar("ModelTypeT", bound=UUIDAuditBase)
CreateSchemaTypeT = TypeVar("CreateSchemaTypeT", bound=BaseModel)
UpdateSchemaTypeT = TypeVar("UpdateSchemaTypeT", bound=BaseModel)


class InsertOnlyBase(Generic[ModelTypeT, CreateSchemaTypeT]):
    """Base class that supports Create and Read methods but not Update or Delete."""

    def __init__(self, model: Type[ModelTypeT]) -> None:
        """Init the InsertOnlyBase class with a given SQLAlchemy model."""
        self.model = model

    def get(self, db: Session, row_id: UUID) -> ModelTypeT | None:
        """
        Use the primary key to return a single record from the table.

        Parameters
        ----------
        db: Session
            Instance of SQLAlchemy session that manages database transactions
        row_id: UUID
            The value of the primary key used to retrieve the record

        Returns
        -------
        ModelTypeT | None
            Returns an instance of the SQLAlchemy model being queried if a row
            is found for the primary key value passed, or None otherwise

        """
        return db.get(self.model, row_id)

    def get_first(self, db: Session, query: sa.Select) -> ModelTypeT | None:
        """Return the first row of the query provided."""
        return db.scalar(query)

    def get_count(self, db: Session) -> int:
        """Return the count of rows in the table, or the query if one is given."""
        stmt = sa.select(sa.func.count()).select_from(self.model)  # pylint: disable=not-callable  # fmt: skip
        count = db.execute(stmt).scalar()
        if count:
            return count
        return 0

    def get_all(
        self,
        db: Session,
        query: sa.Select | None = None,
    ) -> Sequence[ModelTypeT]:
        """
        Return all rows in the table, or from the query if one is provided.

        Parameters
        ----------
        db: Session
            Instance of SQLAlchemy session that manages database transactions
        query: Select | None
            SQLAlchemy query to fetch all records from. If a query isn't provided,
            the method will return all records in the table by default

        Returns
        -------
        Sequence[ModelTypeT]
            Returns a list of instances of the SQLAlchemy model being queried

        """
        if query is None:
            query = self.query_all()
        return db.execute(query).scalars().all()

    def query_all(self) -> sa.Select:
        """Return a query of all records that can be paginated."""
        return sa.select(self.model)

    def create(
        self,
        db: Session,
        *,
        data: CreateSchemaTypeT,  # must be passed as keyword argument
        defer_commit: bool = False,  # optionally defer commit
    ) -> ModelTypeT:
        """
        Insert a new row into the table.

        Parameters
        ----------
        db: Session
            Instance of SQLAlchemy session that manages database transactions
        data: CreateSchemaTypeT
            The instance of the Pydantic schema that contains the data used to
            insert a new row in the database
        defer_commit: bool
            Optionally defer committing this new record. This allows users to
            create multiple records in a single transaction block and roll back
            all creations if one fails.

        """
        record = self.model(id=uuid4(), **data.model_dump())
        if defer_commit:
            return record
        return self.commit_changes(db, record)

    def commit_changes(
        self,
        db: Session,
        record: ModelTypeT,
    ) -> ModelTypeT:
        """Add changes to a session, commits them, and refreshes the record."""
        db.add(record)
        db.commit()
        db.refresh(record)  # issues a SELECT stmt to refresh values of record
        return record


class CRUDBase(
    Generic[ModelTypeT, CreateSchemaTypeT, UpdateSchemaTypeT],
    InsertOnlyBase[ModelTypeT, CreateSchemaTypeT],
):
    """
    CRUD class with default methods to Create, Read, Update, Delete (CRUD).

    Parameters
    ----------
    model: Type[ModelTypeT]
        A SQLAlchemy model class for which CRUD operations will be supported
    schema: Type[BaseModel]
        A Pydantic model (schema) class to use to return the

    """

    def __init__(self, model: Type[ModelTypeT]) -> None:
        """Init the CRUD class with a given SQLAlchemy model."""
        super().__init__(model=model)

    def update(
        self,
        db: Session,
        *,
        record: ModelTypeT,
        update_data: UpdateSchemaTypeT,
    ) -> ModelTypeT:
        """
        Update a record in the table.

        Parameters
        ----------
        db: Session
            Instance of SQLAlchemy session that manages database transactions
        record: ModelTypeT
            Instance of the SQLAlchemy model that represents the row in the
            corresponding database table that will be updated
        update_data: UpdateSchemaTypeT
            Either an instance of a Pydantic schema or a dictionary of values
            used to update the row in the database

        """
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(record, field, value)
        return self.commit_changes(db, record)

    def delete(self, db: Session, *, row_id: UUID) -> None:
        """
        Delete a record from the table.

        Parameters
        ----------
        db: Session
            Instance of SQLAlchemy session that manages database transactions
        row_id: UUID
            The primary key value of the row that will be deleted

        """
        record = db.get(self.model, row_id)
        db.delete(record)
        db.commit()
