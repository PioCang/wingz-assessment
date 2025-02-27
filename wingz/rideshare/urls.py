from django.urls import path

from .views.auth import UserLoginView, UserLogoutView, UserSignupView
from .views.rides import RideEventViewSet, RideViewSet, UserViewSet

user_list = UserViewSet.as_view({"get": "list", "post": "create"})
user_detail = UserViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

ride_list = RideViewSet.as_view({"get": "list", "post": "create"})
ride_detail = RideViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

ride_event_list = RideEventViewSet.as_view({"get": "list", "post": "create"})
ride_event_detail = RideEventViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    # Auth endpoints
    path("auth/signup/", UserSignupView.as_view(), name="signup"),
    path("auth/login/", UserLoginView.as_view(), name="login"),
    path("auth/logout/", UserLogoutView.as_view(), name="logout"),
    # User endpoints
    path("users/", user_list, name="user-list"),
    path("users/<int:pk>/", user_detail, name="user-detail"),
    # Ride endpoints
    path("rides/", ride_list, name="ride-list"),
    path("rides/<int:pk>/", ride_detail, name="ride-detail"),
    # RideEvent endpoints
    path("ride-events/", ride_event_list, name="rideevent-list"),
    path("ride-events/<int:pk>/", ride_event_detail, name="rideevent-detail"),
]
