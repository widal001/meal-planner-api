"""Route API requests related to managing recipes and their ingredients."""

from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination.links import Page
from sqlalchemy.orm import Session

from meal_planner.dependencies.database import get_db
from meal_planner.models.recipe import Recipe
from meal_planner.schemas.recipe import RecipeCreateSchema, RecipeDumpSchema
from meal_planner.services.recipes import recipe_service

recipe_router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)


@recipe_router.get(
    "/",
    summary="Get a list of recipes",
    response_model=Page[RecipeDumpSchema],
    status_code=status.HTTP_200_OK,
)
def list_recipes(db: Annotated[Session, Depends(get_db)]) -> Sequence[Recipe]:
    """Fetch summary-level information about a list of recipes."""
    return paginate(conn=db, query=recipe_service.query_all())


@recipe_router.post(
    "/",
    summary="Create a recipe",
    response_model=RecipeDumpSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_a_recipe(
    db: Annotated[Session, Depends(get_db)],
    payload: RecipeCreateSchema,
) -> Recipe:
    """Create a new recipe."""
    return recipe_service.create(db, data=payload)


@recipe_router.get(
    "/{recipe_id}",
    summary="Get recipe details",
    response_model=RecipeDumpSchema,
    status_code=status.HTTP_200_OK,
)
def get_recipe_by_id(
    db: Annotated[Session, Depends(get_db)],
    recipe_id: UUID,
) -> Recipe:
    """Fetch the details for a specific recipe using its id."""
    recipe = recipe_service.get(db=db, row_id=recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )
    return recipe
