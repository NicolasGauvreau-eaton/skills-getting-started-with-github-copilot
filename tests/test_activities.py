"""Tests for GET /activities endpoint using AAA pattern"""


def test_get_activities_success(client, fresh_activities):
    """
    Arrange: Client is ready
    Act: Call GET /activities
    Assert: Response contains all activities with correct structure
    """
    # Arrange
    # (setup is in fixtures)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_structure(client, fresh_activities):
    """
    Arrange: Client is ready
    Act: Call GET /activities
    Assert: Response data has correct structure with all required fields
    """
    # Arrange
    # (setup is in fixtures)

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_with_participants(client, fresh_activities):
    """
    Arrange: Client is ready, activities have participants
    Act: Call GET /activities
    Assert: Participant lists are returned correctly
    """
    # Arrange
    # (setup is in fixtures)

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert len(data["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
