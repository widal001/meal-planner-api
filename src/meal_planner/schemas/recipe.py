"""Manage schemas for recipes."""

from pydantic import BaseModel, ConfigDict

from meal_planner.schemas.ingredient import IngredientBaseSchema


class RecipeBaseSchema(BaseModel):
    """Recipe schema with shared fields."""

    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class RecipeIngredient(IngredientBaseSchema):
    """An ingredient in a recipe."""

    food: str


class RecipeCreateSchema(RecipeBaseSchema):
    """Schema used to create new recipes."""

    ingredients: list[RecipeIngredient]


class RecipeUpdateSchema(RecipeBaseSchema):
    """Schema used to update recipes."""
