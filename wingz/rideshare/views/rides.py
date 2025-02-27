from rest_framework import viewsets
from rideshare.models import Ride, RideEvent, User
from rideshare.permissions import IsAdminUser
from rideshare.serializers import (
    RideEventSerializer,
    RideSerializer,
    UserSerializer,
)

from .pagination import BasicPagination


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination


class RideViewSet(viewsets.ModelViewSet):
    """API endpoint that allows rides to be viewed or edited."""

    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination


class RideEventViewSet(viewsets.ModelViewSet):
    """API endpoint that allows ride events to be viewed or edited."""

    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination
