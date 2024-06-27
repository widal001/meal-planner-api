"""Test the recipe_router."""

from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from tests.utils import test_data


class TestListRecipes:
    """Test the GET /recipes/ endpoint."""

    ENDPOINT = "/recipes/"

    def test_response_code_is_200(self, client: TestClient):
        """The status code should be 200."""
        # execution
        response = client.get(self.ENDPOINT)
        # validation
        print(response.json()["items"][0])
        assert response.status_code == 200

    def test_response_should_be_paginated(self, client: TestClient):
        """The endpoint response should be paginated."""
        # execution
        response_body = client.get(self.ENDPOINT).json()
        # validation
        assert response_body.get("page") == 1  # page defaults to 1
        assert response_body.get("size") == 50  # size defaults to 50
        assert isinstance(response_body.get("items"), list)
        assert isinstance(response_body.get("links"), dict)

    def test_change_item_count_with_pagination_params(
        self,
        client: TestClient,
    ):
        """The number of items returned should be influenced by size param."""
        # setup
        params = {"size": 1, "page": 1}
        # execution
        response_body = client.get(self.ENDPOINT, params=params).json()
        # validation
        assert len(response_body["items"]) == 1
        assert response_body["links"]["next"] is not None
        assert response_body["links"]["prev"] is None


class TestPostRecipe:
    """Test the POST /recipes/ endpoint."""

    ENDPOINT = "/recipes/"

    def test_return_status_code_201_if_successful(
        self,
        client: TestClient,
    ):
        """A successful response should return status code 201."""
        # setup
        payload = {
            "name": "Test recipe",
            "description": "This is a test description.",
            "ingredients": [
                {"food": "Onion", "amount": 2, "unit": "self"},
                {"food": "Salt", "amount": 0.5, "unit": "tsp"},
            ],
        }
        # execution
        response = client.post(self.ENDPOINT, json=payload)
        response_body = response.json()
        # validation
        assert response.status_code == 201
        assert response_body["name"] == "Test recipe"

    def test_return_status_code_422_if_required_field_is_missing(
        self,
        client: TestClient,
    ):
        """If a required field is missing, return status code 422."""
        # setup
        payload = {
            "name": "Test recipe with missing handle",
            "tags": ["a", "b"],
        }
        # execution
        response = client.post(self.ENDPOINT, json=payload)
        # validation - check that status code is 422
        assert response.status_code == 422


class TestGetRecipeById:
    """Test the GET /recipes/<recipe_id> endpoint."""

    DEFAULT = test_data.SALSA

    def endpoint(self, recipe_id: UUID) -> str:
        """Make the endpoint path to test."""
        return f"/recipes/{recipe_id}"

    def test_return_correct_recipe(self, client: TestClient):
        """The correct recipe should be returned."""
        # setup
        endpoint = self.endpoint(self.DEFAULT)
        wanted = test_data.RECIPES[self.DEFAULT]
        # execution
        response = client.get(endpoint)
        print(response.json())
        # validation
        assert response.status_code == 200
        assert response.json()["name"] == wanted["name"]

    def test_return_404_if_id_has_no_match(self, client: TestClient):
        """Return 404 if id provided doesn't have a database match."""
        # setup - use an id that doesn't match an existing record
        endpoint = self.endpoint(uuid4())
        # execution
        response = client.get(endpoint)
        # validation - response code should be 404
        assert response.status_code == 404
        assert response.json() == {"detail": "Recipe not found"}
