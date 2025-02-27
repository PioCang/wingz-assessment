import pytest
from rideshare.enums import UserRoleChoices


@pytest.mark.django_db
class TestUsers:
    def test_get_users_list(self, authenticated_client):
        response = authenticated_client.get("/users/")
        assert response.status_code == 200

    def test_create_user(self, authenticated_client):
        payload = {
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "new@example.com",
            "phone_number": "+639231234567",
            "role": UserRoleChoices.REGULAR,
            "password": "securepass",
        }
        response = authenticated_client.post("/users/", payload)
        assert response.status_code == 201
        assert response.data["username"] == "newuser"
