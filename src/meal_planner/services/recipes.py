"""Handle the business logic for reading and creating recipes."""

from uuid import uuid4

from sqlalchemy.orm import Session

from meal_planner.models.recipe import Recipe
from meal_planner.schemas.ingredient import IngredientCreateSchema
from meal_planner.schemas.recipe import (
    RecipeCreateSchema,
    RecipeIngredient,
    RecipeUpdateSchema,
)
from meal_planner.services.base import CRUDBase
from meal_planner.services.ingredients import ingredient_service


class RecipeService(CRUDBase[Recipe, RecipeCreateSchema, RecipeUpdateSchema]):
    """Handle the business logic for reading and creating recipes."""

    def create(
        self,
        db: Session,
        *,
        data: RecipeCreateSchema,
        defer_commit: bool = False,
    ) -> Recipe:
        """Create a new recipe."""
        recipe = Recipe(id=uuid4(), **data.model_dump(exclude={"ingredients"}))
        for ingredient in data.ingredients:
            self.add_ingredient(db, recipe, ingredient)
        if defer_commit:
            return recipe
        return self.commit_changes(db, recipe)

    def add_ingredient(
        self,
        db: Session,
        recipe: Recipe,
        ingredient: RecipeIngredient,
    ) -> None:
        """Create and add an ingredient record to a recipe."""
        data = IngredientCreateSchema(
            recipe_id=recipe.id,
            food=ingredient.food,
            amount=ingredient.amount,
            unit=ingredient.unit,
        )
        record = ingredient_service.create(db=db, data=data, defer_commit=True)
        recipe.ingredients.append(record)


recipe_service = RecipeService(model=Recipe)
