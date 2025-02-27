"""Serializers used by the REST endpoints"""

from rest_framework import serializers

from .models import User


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
