"""Serializers used by the REST endpoints"""

from rest_framework import serializers

from .models import Ride, RideEvent, User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

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
            "password",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password") or None
        if password:
            # We cannot accept blank passwords
            instance.set_password(password)
        return super().update(instance, validated_data)


class RideBasicSerializer(serializers.ModelSerializer):
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
        ]
        read_only_fields = ["id"]


class RideComplexSerializer(serializers.ModelSerializer):
    rider = UserSerializer(read_only=True)
    driver = UserSerializer(read_only=True)
    distance = serializers.FloatField(read_only=True)
    todays_ride_events = serializers.SerializerMethodField()

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
            "distance",
            "todays_ride_events",
        ]
        read_only_fields = ["id"]

    def get_todays_ride_events(self, obj):
        if hasattr(obj, "todays_ride_events"):
            return RideEventSerializer(obj.todays_ride_events, many=True).data
        return []


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = [
            "id",
            "ride",
            "description",
            "created_at",
        ]
        read_only_fields = ["id"]
