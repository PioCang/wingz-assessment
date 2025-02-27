import pytest
from rideshare.models import User


@pytest.mark.django_db
class TestIsAdminUserPermission:
    @pytest.fixture
    def regular_user(self):
        return User.objects.create_user(
            username="regular_user",
            email="user@example.com",
            password="userpass",
            role="regular",
        )

    @pytest.fixture
    def authenticated_admin_client(self, api_client, create_users):
        """Authenticate an admin user."""
        admin_user, _ = create_users
        api_client.force_authenticate(user=admin_user)
        return api_client

    @pytest.fixture
    def authenticated_regular_client(self, api_client, regular_user):
        """Authenticate a regular user."""
        api_client.force_authenticate(user=regular_user)
        return api_client

    def test_admin_access(self, authenticated_client):
        """Ensure an admin user has access."""
        response = authenticated_client.get("/users/")
        assert response.status_code == 200  # Admin should have access

    def test_regular_user_denied(self, authenticated_regular_client):
        """Ensure a regular user is denied access."""
        response = authenticated_regular_client.get("/users/")
        assert response.status_code == 403  # Regular user should be forbidden

    def test_unauthenticated_user_denied(self, api_client):
        """Ensure an unauthenticated user is denied access."""
        response = api_client.get("/users/")
        assert (
            response.status_code == 401
        )  # Unauthenticated should be unauthorized
