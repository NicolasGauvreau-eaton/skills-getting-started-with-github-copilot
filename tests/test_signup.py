"""Tests for POST /activities/{activity}/signup endpoint using AAA pattern"""


def test_signup_success(client, fresh_activities):
    """
    Arrange: Client ready, new email to sign up
    Act: POST signup for an activity
    Assert: Student is added to participants
    """
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    initial_count = len(fresh_activities[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
    assert new_email in fresh_activities[activity_name]["participants"]
    assert len(fresh_activities[activity_name]["participants"]) == initial_count + 1


def test_signup_duplicate_email(client, fresh_activities):
    """
    Arrange: Client ready, student already registered
    Act: POST signup with duplicate email
    Assert: 400 error with appropriate message
    """
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "michael@mergington.edu"  # Already in Chess Club

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": duplicate_email}
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_invalid_activity(client, fresh_activities):
    """
    Arrange: Client ready, nonexistent activity name
    Act: POST signup to invalid activity
    Assert: 404 error with activity not found message
    """
    # Arrange
    invalid_activity = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{invalid_activity}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_signup_email_format_accepted(client, fresh_activities):
    """
    Arrange: Client ready, various email formats
    Act: POST signup with different email formats
    Assert: All valid formats are accepted (no email validation on backend)
    """
    # Arrange
    activity_name = "Programming Class"
    test_emails = [
        "simple@example.com",
        "with.dot@example.co.uk",
        "with+tag@example.com",
    ]

    # Act & Assert
    for email in test_emails:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
