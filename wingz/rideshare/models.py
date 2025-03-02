from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .enums import RideStatusChoices, UserRoleChoices


class User(AbstractUser):
    """Represents a user on the platform.

    Email field is an alternate primary key.
    We don't delete Users, instead we soft-delete using the `is_active` tag.
    """

    is_active = models.BooleanField(default=True)
    role = models.CharField(
        max_length=32,
        choices=UserRoleChoices,
        default=UserRoleChoices.REGULAR,
    )
    first_name = models.CharField(max_length=64, blank=True, null=False)
    last_name = models.CharField(max_length=64, blank=True, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = PhoneNumberField(blank=True, null=False)


class Ride(models.Model):
    """Represents details of a Ride."""

    status = models.CharField(
        max_length=32,
        choices=RideStatusChoices,
        default=RideStatusChoices.INIT,
    )
    rider = models.ForeignKey(
        User, related_name="rides_as_rider", on_delete=models.PROTECT
    )
    driver = models.ForeignKey(
        User, related_name="rides_as_driver", on_delete=models.PROTECT
    )
    pickup_latitude = models.FloatField(default=0.0, null=False)
    pickup_longitude = models.FloatField(default=0.0, null=False)
    dropoff_latitude = models.FloatField(default=0.0, null=False)
    dropoff_longitude = models.FloatField(default=0.0, null=False)
    pickup_time = models.DateTimeField(blank=True, null=False)


class RideEvent(models.Model):
    """Represents an Event that takes place over the course of a Ride"""

    created_at = models.DateTimeField(blank=False, null=False)
    ride = models.ForeignKey(
        Ride, related_name="ride_events", on_delete=models.CASCADE
    )
    description = models.CharField(max_length=1024, blank=True, null=False)
