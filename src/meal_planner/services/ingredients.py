"""Handle business logic for ingredients."""

from uuid import uuid4

from sqlalchemy.orm import Session

from meal_planner.models.ingredient import Ingredient
from meal_planner.schemas.ingredient import IngredientCreateSchema
from meal_planner.services.base import InsertOnlyBase
from meal_planner.services.foods import food_service


class IngredientService(InsertOnlyBase[Ingredient, IngredientCreateSchema]):
    """Handle the business logic for reading and creating ingredients."""

    def create(
        self,
        db: Session,
        *,
        data: IngredientCreateSchema,
        defer_commit: bool = False,
    ) -> Ingredient:
        """Create a new ingredient."""
        # create the ingredient
        ingredient = Ingredient(
            id=uuid4(),
            **data.model_dump(exclude={"food"}),
        )
        # connect it to its parent food
        ingredient.food = food_service.get_or_create_by_name(db, data.food)
        # optionally commit and return the record
        if defer_commit:
            db.add(ingredient)
            return ingredient
        return self.commit_changes(db, ingredient)


ingredient_service = IngredientService(model=Ingredient)
