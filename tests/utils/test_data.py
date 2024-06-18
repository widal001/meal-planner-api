"""Create mock data to populate the database for testing."""

from dataclasses import dataclass
from uuid import UUID, uuid4

from meal_planner.models.base import UUIDAuditBase
from meal_planner.models.food import Food
from meal_planner.models.recipe import Recipe


@dataclass
class MockTableData:
    """Map test data to the model used to populate that test data in the db."""

    model: type[UUIDAuditBase]
    records: dict[UUID, dict]


#########
# Foods #
#########
BEAN = uuid4()
CORN = uuid4()
SALT = uuid4()
ONION = uuid4()
STEAK = uuid4()
PEPPER = uuid4()
TOMATO = uuid4()
TORTILLA = uuid4()
FOODS = {
    BEAN: {"name": "Black beans", "kind": "Canned"},
    CORN: {"name": "Sweet corn", "kind": "Canned"},
    SALT: {"name": "Salt", "kind": "Spices"},
    ONION: {"name": "Onion", "kind": "Produce"},
    PEPPER: {"name": "Red pepper", "kind": "Produce"},
    TOMATO: {"name": "Tomato", "kind": "Produce"},
    STEAK: {"name": "Steak", "kind": "Meat"},
    TORTILLA: {"name": "Corn tortillas", "kind": "Grocery"},
}

###########
# Recipes #
###########
SALSA = uuid4()
FAJITAS = uuid4()
TACOS = uuid4()
RECIPES = {
    SALSA: {
        "name": "Zesty salsa",
        "description": "Instructions for zesty salsa",
    },
    FAJITAS: {
        "name": "Steak fajitas",
        "description": "Instructions for steak fajitas",
    },
    TACOS: {
        "name": "Black bean and corn tacos",
        "description": "Instructions for black bean and corn tacos",
    },
}

###############
# Ingredients #
###############
INGREDIENTS = {
    SALSA: {
        ONION: {"amount": 0.5, "unit": "self"},
        SALT: {"amount": 0.25, "unit": "tsp"},
        PEPPER: {"amount": 0.5, "unit": "self"},
        TOMATO: {"amount": 2, "unit": "self"},
    },
    FAJITAS: {
        ONION: {"amount": 1.5, "unit": "self"},
        PEPPER: {"amount": 2, "unit": "self"},
        STEAK: {"amount": 8, "unit": "oz"},
        TORTILLA: {"amount": 6, "unit": "self"},
    },
    TACOS: {
        ONION: {"amount": 1, "unit": "self"},
        BEAN: {"amount": 2, "unit": "cup"},
        CORN: {"amount": 14, "unit": "oz"},
        TORTILLA: {"amount": 6, "unit": "self"},
    },
}

# records to create and insert directly
UUID_TABLES = {
    "food": MockTableData(model=Food, records=FOODS),
    "recipes": MockTableData(model=Recipe, records=RECIPES),
}
