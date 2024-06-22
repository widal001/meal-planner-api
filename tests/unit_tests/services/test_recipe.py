"""Test the RecipeService class."""

from sqlalchemy.orm import Session

from meal_planner.services.recipe import recipe_service
from meal_planner.services.food import food_service
from meal_planner.schemas.recipe import RecipeCreateSchema, RecipeIngredient


def ingredient(
    db: Session,
    *,
    food: str,
    should_exist: bool,
) -> RecipeIngredient:
    """Return a RecipeIngredient and check whether or not it already exists."""
    food_record = food_service.get_by_name(db, food)
    if should_exist:
        assert food_record is not None
    else:
        assert food_record is None
    return RecipeIngredient(food=food, amount=1, unit="self")


class TestCreate:
    """Test the create() method."""

    def test_do_not_create_new_food_if_ingredient_exists(
        self,
        test_session: Session,
    ):
        """Don't create a new food record if the ingredients already exist."""
        # arrange - create test data
        ingredients = [
            ingredient(test_session, food="Salt", should_exist=True),
            ingredient(test_session, food="Red pepper", should_exist=True),
            ingredient(test_session, food="Onion", should_exist=True),
        ]
        data = RecipeCreateSchema(
            name="New recipe",
            description="This is a new test recipe.",
            ingredients=ingredients,
        )
        # arrange - get the current recipe and food count
        recipe_count_old = recipe_service.get_count(test_session)
        food_count_old = food_service.get_count(test_session)
        # act
        recipe = recipe_service.create(test_session, data=data)
        recipe_count_new = recipe_service.get_count(test_session)
        food_count_new = food_service.get_count(test_session)
        # assert
        assert recipe is not None
        assert recipe_count_new == recipe_count_old + 1
        assert food_count_new == food_count_old

    def test_create_new_food_record_if_ingredient_does_not_exist(
        self,
        test_session: Session,
    ):
        """Don't create a new food record if the ingredients already exist."""
        # arrange - create test data
        ingredients = [
            ingredient(test_session, food="Lime", should_exist=False),
            ingredient(test_session, food="Red pepper", should_exist=True),
            ingredient(test_session, food="Onion", should_exist=True),
        ]
        data = RecipeCreateSchema(
            name="New recipe",
            description="This is a new test recipe.",
            ingredients=ingredients,
        )
        # arrange - get the current recipe and food count
        recipe_count_old = recipe_service.get_count(test_session)
        food_count_old = food_service.get_count(test_session)
        # act
        recipe = recipe_service.create(test_session, data=data)
        recipe_count_new = recipe_service.get_count(test_session)
        food_count_new = food_service.get_count(test_session)
        # assert
        assert recipe is not None
        assert recipe_count_new == recipe_count_old + 1
        assert food_count_new == food_count_old + 1
