"""Test the database connection."""

from sqlalchemy.orm import Session
from sqlalchemy import text


def test_that_mock_session_is_active(test_session: Session):
    """Test that the test_session fixture has a live connection to the test db."""
    # act
    result = test_session.scalar(text("SELECT 1"))
    # assert
    assert result == 1
