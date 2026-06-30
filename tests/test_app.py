from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

INITIAL_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = deepcopy(INITIAL_ACTIVITIES)
    yield
    app_module.activities = deepcopy(INITIAL_ACTIVITIES)


def test_root_redirects_to_the_static_index_page():
    # Arrange
    client = TestClient(app_module.app)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_unregister_participant_from_activity():
    # Arrange
    client = TestClient(app_module.app)
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/Chess%20Club/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from Chess Club"
    }
    assert email not in app_module.activities["Chess Club"]["participants"]
