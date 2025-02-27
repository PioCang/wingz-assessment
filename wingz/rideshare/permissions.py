"""Custom DRF permissions"""

from rest_framework.permissions import IsAuthenticated

from .enums import UserRoleChoices
from .models import User


class IsAdminUser(IsAuthenticated):
    """Permissions of Authenticated Admin Users"""

    def has_permission(self, request, view):
        authenticated = super().has_permission(request, view)
        if not authenticated:
            return False

        user: User = request.user
        return user.role == UserRoleChoices.ADMIN
