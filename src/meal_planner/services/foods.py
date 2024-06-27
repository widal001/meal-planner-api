"""Handle business logic for food."""

import sqlalchemy as sa
from sqlalchemy.orm import Session

from meal_planner.models.food import Food
from meal_planner.schemas.food import FoodCreateSchema
from meal_planner.services.base import InsertOnlyBase


class FoodService(InsertOnlyBase[Food, FoodCreateSchema]):
    """Handle the business logic for reading and creating recipes."""

    def get_or_create_by_name(self, db: Session, name: str) -> Food:
        """Find or create a food by its name."""
        food = self.get_by_name(db, name)
        if food:
            return food
        return self.create(
            db,
            data=FoodCreateSchema(name=name),
            defer_commit=True,
        )

    def get_by_name(self, db: Session, name: str) -> Food | None:
        """Find food by name."""
        stmt = sa.select(Food).where(Food.name == name)
        return self.get_first(db, stmt)


food_service = FoodService(model=Food)
