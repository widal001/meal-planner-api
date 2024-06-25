# pylint: disable=no-member
"""Manage schemas for recipes."""

from pydantic import BaseModel, ConfigDict, Field, computed_field

from meal_planner.schemas.food import FoodBaseSchema
from meal_planner.schemas.ingredient import IngredientBaseSchema


class RecipeBaseSchema(BaseModel):
    """Recipe schema with shared fields."""

    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


################
# CRUD schemas #
################


class RecipeIngredient(IngredientBaseSchema):
    """An ingredient in a recipe."""

    food: str


class RecipeCreateSchema(RecipeBaseSchema):
    """Schema used to create new recipes."""

    ingredients: list[RecipeIngredient]


class RecipeUpdateSchema(RecipeBaseSchema):
    """Schema used to update recipes."""


################
# Dump schemas #
################


class RecipeIngredientDumpSchema(IngredientBaseSchema):
    """Schema used to serialize recipe ingredients for API responses."""

    food_record: FoodBaseSchema = Field(validation_alias="food", exclude=True)

    @computed_field
    def food(self) -> str:
        """Pluck the name of the ingredient's food."""
        return self.food_record.name


class RecipeDumpSchema(RecipeBaseSchema):
    """Schema used to serialize recipes for API responses."""

    ingredients: list[RecipeIngredientDumpSchema]
