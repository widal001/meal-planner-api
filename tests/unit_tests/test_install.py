"""Test that the package was installed correctly."""

import meal_planner


def test_package_named_correctly():
    """The package should be imported and named correctly."""
    assert meal_planner.__name__ == "meal_planner"
