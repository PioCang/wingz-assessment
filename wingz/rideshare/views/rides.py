from datetime import timedelta

from django.db.models import (
    ExpressionWrapper,
    F,
    FloatField,
    Prefetch,
    QuerySet,
    Value,
)
from django.db.models.functions import ASin, Cos, Power, Radians, Sin, Sqrt
from django.http import QueryDict
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rideshare.enums import RideStatusChoices
from rideshare.models import Ride, RideEvent, User
from rideshare.permissions import IsAdminUser
from rideshare.serializers import (
    RideBasicSerializer,
    RideComplexSerializer,
    RideEventSerializer,
    UserSerializer,
)

from .pagination import BasicPagination


class UserViewSet(ModelViewSet):
    """API endpoint that allows users to be viewed or edited."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination


class RideViewSet(ModelViewSet):
    """API endpoint that allows rides to be viewed or edited."""

    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination

    def get_serializer_class(self, *args, **kwargs):
        """Use the more complex serialiizer for GET requests"""
        if self.action == "list":
            return RideComplexSerializer
        return RideBasicSerializer

    def get_queryset(self):
        """Custom implementation as specified by instructions

        The order of operations matter, keep this in mind as this could carry
        a performance penalty if fumbled.
        """

        query_params = self.request.GET
        queryset = Ride.objects.select_related("rider").select_related(
            "driver"
        )
        queryset = self.apply_filter_on_status(queryset, query_params)
        queryset = self.apply_filter_on_email(queryset, query_params)
        queryset = self.apply_distance_annotation(queryset, query_params)

        queryset = self.apply_sort_key(queryset, query_params)

        # Apply prefetch last, so that the Rides queryset will be as lean as
        # can be before the secondary database query.
        queryset = self.apply_prefetch_on_ride_events(queryset)

        return queryset

    def apply_filter_on_status(
        self, queryset: QuerySet, query_params: QueryDict
    ) -> QuerySet:
        """Apply a filter lookup depending on given `status` parameter.

        Status filter matching is case-sensitive.
        """

        status = query_params.get("status") or ""
        if not status:
            return queryset

        if status not in RideStatusChoices:
            raise ValidationError(
                f"status must be in {str(RideStatusChoices.values)}"
            )

        return queryset.filter(status=status)

    def apply_filter_on_email(
        self, queryset: QuerySet, query_params: QueryDict
    ) -> QuerySet:
        """Apply a filter lookup depending on given `email` parameter

        Email filter matching is case-insensitive.
        """

        email = query_params.get("email") or ""
        if not email:
            return queryset

        return queryset.filter(rider__email__iexact=email)

    def apply_distance_annotation(
        self, queryset: QuerySet, query_params: QueryDict
    ) -> QuerySet:
        """Compute the distance between the input coordinates and the pickup
        coordinates using the Haversine formula:

        6371
        * 2
        *
        ASIN(
            SQRT(
                POWER(
                    SIN(RADIANS(present_latitude - pickup_latitude) / 2)
                    , 2
                )
                + COS(RADIANS(pickup_latitude))
                * COS(RADIANS(present_latitude)) *
                POWER(
                    SIN(RADIANS(present_longitude - pickup_longitude) / 2)
                    , 2
                )
            )
        )
        """
        input_latitude = query_params.get("lat") or None
        input_longitude = query_params.get("lon") or None

        if not all([input_latitude, input_longitude]):
            raise ValidationError("You must provide values for lat and lon")

        try:
            input_latitude = float(input_latitude)
            input_longitude = float(input_longitude)
        except (ValueError, TypeError) as e:
            raise ValidationError("lat and lon must both be float type") from e

        haversine_equation = (
            Value(6371)
            * Value(2)
            * ASin(
                Sqrt(
                    Power(
                        Sin(
                            Radians(
                                Value(input_latitude) - F("pickup_latitude")
                            )
                            / 2
                        ),
                        2,
                    )
                    + Cos(Radians(F("pickup_latitude")))
                    * Cos(Radians(Value(input_latitude)))
                    * Power(
                        Sin(
                            Radians(
                                Value(input_longitude) - F("pickup_longitude")
                            )
                            / 2
                        ),
                        2,
                    )
                )
            )
        )

        queryset = queryset.annotate(
            distance=ExpressionWrapper(
                haversine_equation, output_field=FloatField()
            )
        )

        return queryset

    def apply_sort_key(
        self, queryset: QuerySet, query_params: QueryDict
    ) -> QuerySet:
        """Apply the sort order depending on given `sort_by` parameter"""

        SORT_BY_PICKUP_TIME = "pickup_time"
        SORT_BY_DISTANCE = "distance"

        allowed_sort_keys = (SORT_BY_PICKUP_TIME, SORT_BY_DISTANCE)
        sort_key = query_params.get("sort_by") or SORT_BY_PICKUP_TIME
        if sort_key not in allowed_sort_keys:
            raise ValidationError(
                f"sort_key must be in {str(allowed_sort_keys)}"
            )

        return queryset.order_by(sort_key)

    def apply_prefetch_on_ride_events(self, queryset: QuerySet) -> QuerySet:
        """Prefetch the Ride Events, belonging to the Ride objects, that have
        occurred in the past 24 hours
        """

        twenty_four__hours_ago = timezone.now() - timedelta(hours=24)
        ride_events_in_past_24_hrs = RideEvent.objects.filter(
            created_at__gte=twenty_four__hours_ago
        ).order_by("created_at")
        queryset = queryset.prefetch_related(
            Prefetch(
                "ride_events",
                queryset=ride_events_in_past_24_hrs,
                to_attr="todays_ride_events",
            )
        )
        return queryset


class RideEventViewSet(ModelViewSet):
    """API endpoint that allows ride events to be viewed or edited."""

    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination
