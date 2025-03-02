import pytest
from django.utils import timezone


@pytest.mark.django_db
class TestRideEvents:

    def test_get_ride_events_list(self, authenticated_client, ride_event):
        response = authenticated_client.get("/ride-events/")
        assert response.status_code == 200
        assert len(response.data["results"]) > 0

    def test_create_ride_event(self, authenticated_client, ride):
        client = authenticated_client
        payload = {
            "created_at": timezone.now(),
            "ride": ride.id,
            "description": "Passenger picked up",
        }
        response = client.post("/ride-events/", payload, format="json")
        assert response.status_code == 201
        assert response.data["description"] == "Passenger picked up"
