from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .enums import RideStatusChoices, UserRoleChoices


class TimeStampedModel(models.Model):
    """An abstract base class model that provides self-updating `created_at`
    and `modified_at` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, TimeStampedModel):
    """Represents a user on the platform.

    Email field is an alternate primary key.
    We don't delete Users, instead we soft-delete using the `is_active` tag.
    """

    objects = UserManager()

    username = models.CharField(max_length=64, unique=True)
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


class Ride(TimeStampedModel):
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


class RideEvent(TimeStampedModel):
    """Represents an Event that takes place over the course of a Ride"""

    ride = models.ForeignKey(
        Ride, related_name="ride_events", on_delete=models.CASCADE
    )
    description = models.CharField(max_length=1024, blank=True, null=False)
