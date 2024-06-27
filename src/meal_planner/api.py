"""Instantiate the meal planner API and root-level endpoints."""

from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi_pagination import add_pagination

from meal_planner.routers.recipes import recipe_router

app = FastAPI()
app.include_router(recipe_router)
add_pagination(app)


@app.get("/")
async def root() -> RedirectResponse:
    """Redirects the user to the API docs."""
    return RedirectResponse(
        "/docs",
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )
