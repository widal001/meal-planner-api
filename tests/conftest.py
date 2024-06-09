"""Manage shared fixtures and test settings for pytest."""

import pytest
from fastapi.testclient import TestClient

from meal_planner.api import app


@pytest.fixture(name="client")
def mock_client() -> TestClient:
    """Create a mock client to test the API."""
    return TestClient(app)
