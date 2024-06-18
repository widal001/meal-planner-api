"""Create an ORM for the food table in the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from meal_planner.models.base import UUIDAuditBase

if TYPE_CHECKING:
    from sqlalchemy.orm import Mapped

    from meal_planner.models.ingredient import Ingredient
    from meal_planner.models.recipe import Recipe


class Food(UUIDAuditBase):
    """A dimensional table for foods referenced by grocery lists or recipes."""

    __tablename__ = "food"

    ###########
    # columns #
    ###########

    name: Mapped[str]
    kind: Mapped[str]

    #################
    # relationships #
    #################

    recipes: Mapped[list[Recipe]] = relationship(
        secondary="ingredient",
        viewonly=True,
    )
    recipe_ingredients: Mapped[list[Ingredient]] = relationship(
        back_populates="food",
        cascade="delete",
    )
