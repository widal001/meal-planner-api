"""Create the database models."""

__all__ = [
    "UUIDAuditBase",
    "Food",
    "Ingredient",
    "Recipe",
]

from meal_planner.models.base import UUIDAuditBase
from meal_planner.models.food import Food
from meal_planner.models.ingredient import Ingredient
from meal_planner.models.recipe import Recipe
