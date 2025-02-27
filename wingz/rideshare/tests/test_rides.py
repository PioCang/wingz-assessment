import pytest
from rideshare.enums import RideStatusChoices
from rideshare.models import Ride


@pytest.mark.django_db
class TestRides:
    @pytest.fixture
    def ride(self, rider, driver):
        return Ride.objects.create(
            status=RideStatusChoices.INIT,
            rider=rider,
            driver=driver,
            pickup_latitude=14.5995,
            pickup_longitude=120.9842,
            dropoff_latitude=14.6091,
            dropoff_longitude=121.0223,
            pickup_time="2025-03-01T14:30:00Z",
        )

    def test_get_rides_list(self, authenticated_client, ride):
        response = authenticated_client.get("/rides/")
        assert response.status_code == 200
        assert len(response.data["results"]) > 0

    def test_create_ride(self, authenticated_client, rider, driver):
        payload = {
            "status": RideStatusChoices.INIT,
            "rider": rider.id,
            "driver": driver.id,
            "pickup_latitude": 14.5995,
            "pickup_longitude": 120.9842,
            "dropoff_latitude": 14.6091,
            "dropoff_longitude": 121.0223,
            "pickup_time": "2025-03-01T14:30:00Z",
        }

        response = authenticated_client.post("/rides/", payload, format="json")
        assert response.status_code == 201
        assert response.data["status"] == RideStatusChoices.INIT
