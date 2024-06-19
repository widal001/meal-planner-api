"""Test the Ingredient model."""

from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from meal_planner.models.ingredient import Ingredient

from tests.utils import test_data


def test_successfully_insert_new_ingredient(test_session: Session):
    """Successfully insert new ingredient if both food and recipe exist."""
    # arrange
    ingredient_id = uuid4()
    record = Ingredient(
        id=ingredient_id,
        food_id=test_data.STEAK,
        recipe_id=test_data.TACOS,
        amount=1,
        unit="self",
    )
    # act
    test_session.add(record)
    test_session.commit()
    # assert
    result = test_session.get(Ingredient, ingredient_id)
    assert result is not None
    assert result.food_id == test_data.STEAK
    assert result.recipe_id == test_data.TACOS


def test_raise_error_on_insert_if_parent_food_does_not_exist(
    test_session: Session,
):
    """Attempting to insert a new ingredient whose parent food doesn't exist raises an error."""
    # arrange
    fake_food_id = uuid4()
    record = Ingredient(
        id=uuid4(),
        food_id=fake_food_id,
        recipe_id=test_data.TACOS,
        amount=1,
        unit="self",
    )
    # act
    test_session.add(record)
    # assert
    with pytest.raises(IntegrityError) as failure:
        test_session.commit()
    assert "FOREIGN KEY" in str(failure.value)


def test_raise_error_on_insert_if_parent_recipe_does_not_exist(
    test_session: Session,
):
    """Attempting to insert a new ingredient whose parent food doesn't exist raises an error."""
    # arrange
    fake_recipe_id = uuid4()
    record = Ingredient(
        id=uuid4(),
        recipe_id=fake_recipe_id,
        food_id=test_data.TOMATO,
        amount=1,
        unit="self",
    )
    # act
    test_session.add(record)
    # assert
    with pytest.raises(IntegrityError) as failure:
        test_session.commit()
    assert "FOREIGN KEY" in str(failure.value)
