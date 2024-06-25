"""Test the RecipeService class."""

from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from meal_planner.models.recipe import Recipe
from meal_planner.services.recipes import recipe_service
from meal_planner.services.foods import food_service
from meal_planner.services.ingredients import ingredient_service
from meal_planner.schemas.recipe import RecipeCreateSchema, RecipeIngredient

from tests.utils import test_data


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


class TestBaseMethods:
    """Test the methods inherited from the InsertOnlyBase."""

    RECIPES = test_data.RECIPES
    DEFAULT_RECIPE = test_data.SALSA

    def test_query_all(self, test_session: Session):
        """query_all() should return a select statement for all recipes."""
        # arrange
        count_wanted = len(self.RECIPES)
        items_wanted = set(self.RECIPES.keys())
        # act
        stmt = recipe_service.query_all()
        got = recipe_service.get_all(test_session, query=stmt)
        # assert
        assert len(got) == count_wanted
        assert {row.id for row in got} == items_wanted

    def test_get_all(self, test_session: Session):
        """get_all() should return all recipes by default."""
        # arrange
        count_wanted = len(self.RECIPES)
        items_wanted = set(self.RECIPES.keys())
        # act
        got = recipe_service.get_all(test_session)
        # assert
        assert len(got) == count_wanted
        assert {row.id for row in got} == items_wanted

    def test_get_count(self, test_session: Session):
        """get_count() should return a count of all records in the table."""
        # arrange
        wanted = len(self.RECIPES)
        # act
        got = recipe_service.get_count(test_session)
        # assert
        assert got == wanted

    def test_get_first(self, test_session: Session):
        """get_first() should return the first record from an ordered query."""
        # arrange
        wanted = sorted(self.RECIPES.keys())[0]
        # act
        stmt = select(Recipe).order_by(Recipe.id)
        got = recipe_service.get_first(test_session, query=stmt)
        # assert
        assert got is not None
        assert got.id == wanted

    def test_get(self, test_session: Session):
        """get() should return a record by its primary key."""
        # arrange
        wanted = self.RECIPES[self.DEFAULT_RECIPE]
        # act
        got = recipe_service.get(test_session, row_id=self.DEFAULT_RECIPE)
        # assert
        assert got is not None
        assert got.id == self.DEFAULT_RECIPE
        assert got.name == wanted["name"]

    def test_getting_a_missing_record_returns_none(
        self,
        test_session: Session,
    ):
        """Attempting to get a record that doesn't exist returns None."""
        # arrange
        fake_id = uuid4()
        # act
        got = recipe_service.get(test_session, fake_id)
        # assert
        assert got is None

    def test_delete_cascades_to_ingredients(self, test_session: Session):
        """Deleting a recipe should also delete its ingredients."""
        # arrange
        recipe_id = self.DEFAULT_RECIPE
        ingredient_count_old = ingredient_service.get_count(test_session)
        food_count_old = food_service.get_count(test_session)
        assert recipe_service.get(test_session, recipe_id) is not None
        # act
        recipe_service.delete(test_session, row_id=self.DEFAULT_RECIPE)
        # assert
        ingredient_count_new = ingredient_service.get_count(test_session)
        food_count_new = food_service.get_count(test_session)
        assert recipe_service.get(test_session, recipe_id) is None
        assert ingredient_count_old > ingredient_count_new
        assert food_count_old == food_count_new

    def test_delete_is_idempotent(self, test_session: Session):
        """Attempting to delete a recipe twice should not error."""
        # arrange
        recipe_id = self.DEFAULT_RECIPE
        assert recipe_service.get(test_session, recipe_id) is not None
        # act
        recipe_service.delete(test_session, row_id=self.DEFAULT_RECIPE)
        recipe_service.delete(test_session, row_id=self.DEFAULT_RECIPE)
        # assert
        assert recipe_service.get(test_session, recipe_id) is None


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
