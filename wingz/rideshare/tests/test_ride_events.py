import pytest
from rideshare.models import Ride, RideEvent


@pytest.mark.django_db
class TestRideEvents:

    @pytest.fixture
    def ride(self, rider, driver):
        return Ride.objects.create(
            status="INIT",
            rider=rider,
            driver=driver,
            pickup_latitude=14.5995,
            pickup_longitude=120.9842,
            dropoff_latitude=14.6091,
            dropoff_longitude=121.0223,
            pickup_time="2025-03-01T14:30:00Z",
        )

    @pytest.fixture
    def ride_event(self, ride):
        return RideEvent.objects.create(ride=ride, description="Ride started")

    def test_get_ride_events_list(self, authenticated_client, ride_event):
        response = authenticated_client.get("/ride-events/")
        assert response.status_code == 200
        assert len(response.data["results"]) > 0

    def test_create_ride_event(self, authenticated_client, ride):
        client = authenticated_client
        payload = {"ride": ride.id, "description": "Passenger picked up"}
        response = client.post("/ride-events/", payload, format="json")
        assert response.status_code == 201
        assert response.data["description"] == "Passenger picked up"
