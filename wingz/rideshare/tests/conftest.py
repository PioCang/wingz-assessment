import pytest
from rest_framework.test import APIClient
from rideshare.enums import UserRoleChoices
from rideshare.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin():
    return User.objects.create_user(
        username="admin",
        password="pass",
        email="admin@example.com",
        role=UserRoleChoices.ADMIN,
    )


@pytest.fixture
def rider():
    return User.objects.create_user(
        username="rider", password="pass", email="rider@example.com"
    )


@pytest.fixture
def driver():
    return User.objects.create_user(
        username="driver", password="pass", email="driver@example.com"
    )


@pytest.fixture
def authenticated_client(api_client, admin):
    api_client.force_authenticate(user=admin)
    return api_client
