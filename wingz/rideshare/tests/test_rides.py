import pytest

from rest_framework.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone

from copy import deepcopy

from rideshare.enums import RideStatusChoices
from rideshare.models import Ride
from rideshare.views.rides import RideViewSet


@pytest.mark.django_db
class TestRidesAPI:
    def test_get_rides_list(self, authenticated_client, ride):
        """Get a basic rides list and perform checks to be up to spec"""
        response = authenticated_client.get(
            "/rides/?lat=10.31445&lon=123.9781"
        )
        assert response.status_code == 200
        assert len(response.data["results"]) > 0

        for obj in response.data["results"]:
            assert "rider" in obj and obj["rider"]
            assert "driver" in obj and obj["driver"]
            assert "distance" in obj and obj["distance"] is not None
            assert (
                "todays_ride_events" in obj
                and obj["todays_ride_events"] is not None
            )

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


@pytest.mark.django_db
class TestRidesListUtils:
    """Test that the Rides queryset helper functions"""

    def test_status_filter_no_args(self, ride):
        """No filters, just a plain query"""
        query_params = {}
        queryset = Ride.objects.all()
        results = RideViewSet().apply_filter_on_status(queryset, query_params)

        assert ride in results
        assert len(results) == 1

    def test_status_filter_matched_args(self, ride):
        """Provided status matches a ride"""
        query_params = {"status": ride.status}
        queryset = Ride.objects.all()
        results = RideViewSet().apply_filter_on_status(queryset, query_params)

        assert ride in results
        assert len(results) == 1

    def test_status_filter_unmatched_args(self):
        """Provided status does not match a ride"""
        query_params = {"status": RideStatusChoices.PICKUP}
        queryset = Ride.objects.all()
        results = RideViewSet().apply_filter_on_status(queryset, query_params)

        assert len(results) == 0

    def test_status_filter_unsupported_args(self):
        """Provided status is not supported"""
        query_params = {"status": "unsupported"}
        queryset = Ride.objects.all()

        with pytest.raises(ValidationError, match="status must be"):
            RideViewSet().apply_filter_on_status(queryset, query_params)

    def test_email_filter_no_args(self, ride):
        """No filters, just a plain query"""
        query_params = {}
        queryset = Ride.objects.all()
        results = RideViewSet().apply_filter_on_email(queryset, query_params)

        assert ride in results
        assert len(results) == 1

    def test_email_filter_matched_args(self, ride, rider):
        """Provided email matches a known rider"""
        query_params = {"email": rider.email}
        queryset = Ride.objects.all()
        results = RideViewSet().apply_filter_on_email(queryset, query_params)

        assert ride in results
        assert len(results) == 1

    def test_email_filter_unmatched_args(self):
        """Provided email is not a rider"""
        query_params = {"email": "unmatched@example.com"}
        queryset = Ride.objects.all()
        results = RideViewSet().apply_filter_on_email(queryset, query_params)

        assert len(results) == 0

    @pytest.mark.parametrize("lon", ["", "abc", None])
    @pytest.mark.parametrize("lat", ["", "def", None])
    def test_distance_annotation_invalid_coordinates(self, lat, lon):
        """Provided lat or lon is invalid"""

        query_params = {"lat": lat, "lon": lon}
        queryset = Ride.objects.all()

        if all([lat, lon]):
            expected_str = "must both be float"
        else:
            expected_str = "must provide values"

        with pytest.raises(ValidationError, match=expected_str):
            RideViewSet().apply_distance_annotation(queryset, query_params)

    def test_distance_annotation_valid_coordinates(self, ride):
        """Provided lat and lon inputs yield a valid distance calculation"""
        query_params = {"lat": 45, "lon": 130}
        queryset = Ride.objects.all()
        results = RideViewSet().apply_distance_annotation(
            queryset, query_params
        )

        assert ride in results
        assert len(results) == 1
        assert results[0].distance

    def test_sort_key_invalid(self):
        """Provided sort key is invalid"""
        query_params = {"sort_by": "entropy"}
        queryset = Ride.objects.all()

        with pytest.raises(ValidationError, match="must be in"):
            RideViewSet().apply_sort_key(queryset, query_params)

    @pytest.mark.parametrize("sort_key", ["pickup_time", None])
    def test_sort_key_pickup_time(self, sort_key, ride):
        """Test that results are truly ordered by pickup_time"""

        later_ride = deepcopy(ride)
        later_ride.pickup_time = later_ride.pickup_time + timedelta(seconds=30)
        later_ride.pk = None
        later_ride.save()

        assert ride.pickup_time < later_ride.pickup_time

        query_params = {"sort_by": sort_key}
        queryset = Ride.objects.all()
        results = RideViewSet().apply_sort_key(queryset, query_params)

        assert len(results) == 2
        assert ride == results[0]
        assert later_ride == results[1]

    def test_sort_key_distance(self, ride):
        """Test that results are truly ordered by distance"""

        input_lat, input_lon = 45, 130

        # The farther ride is halfway around the world
        farther_ride = deepcopy(ride)
        farther_ride.pickup_latitude = -1 * input_lat
        farther_ride.pickup_longitude = -1 * input_lon
        farther_ride.pk = None
        farther_ride.save()

        query_params = {
            "lat": input_lat,
            "lon": input_lon,
            "sort_by": "distance",
        }
        queryset = Ride.objects.all()
        queryset = RideViewSet().apply_distance_annotation(
            queryset, query_params
        )
        results = RideViewSet().apply_sort_key(queryset, query_params)

        assert len(results) == 2
        assert ride == results[0]
        assert farther_ride == results[1]
        assert results[0].distance < results[1].distance

    def test_prefetch_captures_only_todays_events(self, ride, ride_event):
        """Test that only Ride Events from the past 24 hours are captured"""

        event_today = deepcopy(ride_event)
        event_today.created_at = timezone.now()
        event_today.pk = None
        event_today.save()

        assert ride_event.created_at < event_today.created_at

        queryset = Ride.objects.all()
        results = RideViewSet().apply_prefetch_on_ride_events(queryset)

        assert len(results) == 1
        today_event_list = results[0].todays_ride_events

        assert len(today_event_list) == 1
        assert ride_event not in today_event_list
        assert event_today == today_event_list[0]
