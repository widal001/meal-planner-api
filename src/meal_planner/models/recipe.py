"""Create an ORM for the meal table in the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship

from meal_planner.models.base import Mapped, UUIDAuditBase

if TYPE_CHECKING:
    from meal_planner.models.ingredient import Ingredient


class Recipe(UUIDAuditBase):
    """A recipe for a meal."""

    __tablename__ = "recipe"

    ###########
    # columns #
    ###########

    name: Mapped[str]
    description: Mapped[str]

    #################
    # relationships #
    #################

    ingredients: Mapped[list[Ingredient]] = relationship(
        back_populates="recipe",
        cascade="delete",
    )
