"""Serializers used by the REST endpoints"""

from rest_framework import serializers

from .models import Ride, RideEvent, User


class UserSignupSerializer(serializers.ModelSerializer):
    """Serializer used for signing up new Users"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone_number",
            "password",
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "is_active",
        ]
        read_only_fields = ["id"]


class RideSerializer(serializers.ModelSerializer):
    rider = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    driver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Ride
        fields = [
            "id",
            "status",
            "rider",
            "driver",
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_latitude",
            "dropoff_longitude",
            "pickup_time",
            "created_at",
            "last_modified_at",
        ]
        read_only_fields = ["id", "created_at", "last_modified_at"]


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = [
            "id",
            "ride",
            "description",
            "created_at",
            "last_modified_at",
        ]
        read_only_fields = ["id", "created_at", "last_modified_at"]
