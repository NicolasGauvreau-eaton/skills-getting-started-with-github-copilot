import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def fresh_activities(monkeypatch):
    """
    Provide fresh activity data for each test.
    Prevents test pollution by isolating state.
    """
    test_activities = copy.deepcopy(activities)
    monkeypatch.setattr("src.app.activities", test_activities)
    return test_activities
