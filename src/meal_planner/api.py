"""Instantiate the meal planner API and root-level endpoints."""

from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
async def root() -> dict:
    """Redirects the user to the API docs."""
    return RedirectResponse(
        "/docs",
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )
