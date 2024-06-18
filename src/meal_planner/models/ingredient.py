"""Create an ORM for the ingredient table in the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from meal_planner.models.base import UUIDAuditBase

if TYPE_CHECKING:
    from meal_planner.models.food import Food
    from meal_planner.models.recipe import Recipe


class Ingredient(UUIDAuditBase):
    """An ingredient in a recipe."""

    __tablename__ = "ingredient"

    ###########
    # columns #
    ###########

    # foreign keys
    food_id: Mapped[str] = mapped_column(
        ForeignKey("food.id"),
        nullable=False,
    )
    recipe_id: Mapped[str] = mapped_column(
        ForeignKey("recipe.id"),
        nullable=False,
    )
    # regular columns
    quantity: Mapped[float]
    unit: Mapped[str]

    #################
    # relationships #
    #################

    food: Mapped[Food] = relationship(back_populates="recipe_ingredients")
    recipe: Mapped[Recipe] = relationship(back_populates="ingredients")
