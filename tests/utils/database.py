"""Create utility functions for the database."""

from uuid import uuid4

from sqlalchemy.orm import Session
from sqlalchemy import text

from meal_planner.models.base import UUIDAuditBase
from meal_planner.models.ingredient import Ingredient

from tests.utils import test_data as data


def create_records_and_add_to_session(
    model: type[UUIDAuditBase],
    records: dict,
    session: Session,
) -> dict[str, UUIDAuditBase]:
    """
    Create records with the data and model provided and add them to the session.

    Parameters
    ----------
    model: type[UUIDAuditBase]
        A subclass of UUIDAuditBase model to use to create the record
    records: list[TestRecord]
        A list of items that map the record id to the record's input data
    session:
        A SQLAlchemy session that will commit the resulting records to the db

    """
    record_map = {}
    for record_id, test_data in records.items():
        record = model(id=record_id, **test_data)
        record_map[record_id] = record
        session.add(record)
    return record_map


def init_test_db(db: Session) -> None:
    """
    Initialize the database for unit testing or for alembic migrations.

    Parameters
    ----------
    db: Session
        An instance of SessionLocal that creates the db engine and organizes
        calls to the database in a transaction

    Warning
    -------
    This function should only ever be called during unit testing because it
    will drop and create all of the tables from metadata. In all other cases
    (integration and QA testing, etc.) use Alembic migrations instead.

    """
    # Drop and recreate all tables
    UUIDAuditBase.metadata.drop_all(bind=db.get_bind())
    UUIDAuditBase.metadata.create_all(bind=db.get_bind())
    # Enable foreign key constraints in SQLite
    db.execute(text("PRAGMA foreign_keys=ON"))


def populate_db(session: Session) -> None:
    """
    Populate the mock database with test data.

    Parameters
    ----------
    session: Session
        A SQLAlchemy session object passed to this function by the fixture

    """
    # populate UUID-based tables
    records = {}
    for table, test_data in data.UUID_TABLES.items():
        records[table] = create_records_and_add_to_session(
            session=session,
            model=test_data.model,
            records=test_data.records,
        )

    # populate ingredients table
    for recipe, test_data in data.INGREDIENTS.items():
        for food, ingredient_data in test_data.items():
            ingredient = Ingredient(
                id=uuid4(),
                food_id=food,
                recipe_id=recipe,
                **ingredient_data,
            )
            session.add(ingredient)

    # commit the changes
    session.commit()
