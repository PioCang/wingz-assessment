"""Enums for Choices used in the app"""

from django.db import models


class UserRoleChoices(models.TextChoices):
    """Allowed roels for User"""

    ADMIN = ("admin", "Admin")
    REGULAR = ("regular", "Regular")


class RideStatusChoices(models.TextChoices):
    """Allowed statuses for Ride"""

    INIT = ("init", "Ride request created.")
    PICKUP = ("pickup", "Driver to pick up rider.")
    ENROUTE = ("enroute", "Ride commenced to destination.")
    DROPOFF = ("droppoff", "Rider dropped off.")
