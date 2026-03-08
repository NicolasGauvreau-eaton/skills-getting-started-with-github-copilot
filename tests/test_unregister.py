"""Tests for DELETE /activities/{activity}/unregister endpoint using AAA pattern"""


def test_unregister_success(client, fresh_activities):
    """
    Arrange: Client ready, student is registered
    Act: DELETE unregister the student
    Assert: Student is removed from participants
    """
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    initial_count = len(fresh_activities[activity_name]["participants"])

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email_to_remove}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email_to_remove} from {activity_name}"
    assert email_to_remove not in fresh_activities[activity_name]["participants"]
    assert len(fresh_activities[activity_name]["participants"]) == initial_count - 1


def test_unregister_not_registered(client, fresh_activities):
    """
    Arrange: Client ready, student not in activity
    Act: DELETE unregister someone not registered
    Assert: 400 error with appropriate message
    """
    # Arrange
    activity_name = "Chess Club"
    email_not_registered = "notregistered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email_not_registered}
    )

    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_invalid_activity(client, fresh_activities):
    """
    Arrange: Client ready, nonexistent activity
    Act: DELETE unregister from invalid activity
    Assert: 404 error with activity not found
    """
    # Arrange
    invalid_activity = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{invalid_activity}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_unregister_last_participant(client, fresh_activities):
    """
    Arrange: Client ready, activity has only one participant
    Act: DELETE unregister the last participant
    Assert: Participant removed, activity becomes empty
    """
    # Arrange
    activity_name = "Basketball Team"
    email = "alex@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert len(fresh_activities[activity_name]["participants"]) == 0


def test_signup_then_unregister_flow(client, fresh_activities):
    """
    Arrange: Client ready
    Act: Signup a student, then unregister them
    Assert: Student added then removed successfully
    """
    # Arrange
    activity_name = "Art Studio"
    email = "flow@mergington.edu"

    # Act - Signup
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    assert email in fresh_activities[activity_name]["participants"]

    # Act - Unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert unregister_response.status_code == 200
    assert email not in fresh_activities[activity_name]["participants"]
