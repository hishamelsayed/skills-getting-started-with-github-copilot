from urllib.parse import quote


def test_get_activities_returns_expected_fields(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["description"].startswith("Learn strategies")
    assert isinstance(payload["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    check_response = client.get("/activities")
    assert email in check_response.json()[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Programming Class"
    email = "duplicate@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup"

    # Act
    first_response = client.post(endpoint, params={"email": email})
    second_response = client.post(endpoint, params={"email": email})

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up"


def test_remove_participant(client):
    # Arrange
    activity_name = "Gym Class"
    email = "removeme@mergington.edu"
    signup_endpoint = f"/activities/{quote(activity_name)}/signup"
    delete_endpoint = f"/activities/{quote(activity_name)}/participants"

    signup_response = client.post(signup_endpoint, params={"email": email})
    assert signup_response.status_code == 200

    # Act
    response = client.delete(delete_endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    check_response = client.get("/activities")
    assert email not in check_response.json()[activity_name]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Art Workshop"
    email = "ghost@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_invalid_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_invalid_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
