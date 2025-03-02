import pytest
import pytz
from datetime import datetime
from rest_framework.test import APIClient
from rideshare.enums import UserRoleChoices, RideStatusChoices
from rideshare.models import User, Ride, RideEvent


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
def ride(rider, driver):
    return Ride.objects.create(
        status=RideStatusChoices.INIT,
        rider=rider,
        driver=driver,
        pickup_latitude=10.3168,
        pickup_longitude=123.8906,
        dropoff_latitude=14.6091,
        dropoff_longitude=121.0223,
        pickup_time=datetime(2025, 3, 1, 0, 0, 0, 0, pytz.UTC),
    )


@pytest.fixture
def ride_event(ride):
    return RideEvent.objects.create(
        ride=ride,
        description="Ride started",
        created_at=datetime(2025, 3, 1, 0, 0, 1, 0, pytz.UTC),
    )


@pytest.fixture
def authenticated_client(api_client, admin):
    api_client.force_authenticate(user=admin)
    return api_client
