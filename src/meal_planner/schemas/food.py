"""Manage schemas for food."""

from pydantic import BaseModel, ConfigDict


class FoodBaseSchema(BaseModel):
    """Schema with shared fields for a food item."""

    name: str

    model_config = ConfigDict(from_attributes=True)


class FoodCreateSchema(FoodBaseSchema):
    """Schema used to create new food."""
