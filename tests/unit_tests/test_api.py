"""Test the API entrypoint and root path."""

from fastapi.testclient import TestClient


def test_root_path_redirects_to_docs(client: TestClient):
    """Test that navigating to the root path "/" automatically redirects to /docs."""
    # act
    response = client.get("/")
    # assert
    assert response.status_code == 200
    assert "/docs" in str(response.url)
