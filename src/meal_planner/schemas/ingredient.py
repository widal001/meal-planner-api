"""Manage schemas for ingredients."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class IngredientBaseSchema(BaseModel):
    """Ingredient schema with base fields."""

    amount: float
    unit: str

    model_config = ConfigDict(from_attributes=True)


class IngredientCreateSchema(IngredientBaseSchema):
    """Schema used to create new ingredients."""

    recipe_id: UUID
    food: str
