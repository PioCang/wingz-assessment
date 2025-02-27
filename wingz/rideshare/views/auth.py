"""

References:
https://medium.com/django-unleashed/token-based-authentication-and-authorization-in-django-rest-framework-user-and-permissions-347c7cc472e9
https://stackoverflow.com/a/64824530
"""

from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rideshare.serializers import UserSignupSerializer


class UserSignupView(generics.CreateAPIView):
    """DRF-provided registration view"""

    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]


class UserLoginView(APIView):
    """Login a user using Token Auth"""

    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data["username"],
            password=request.data["password"],
        )
        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class UserLogoutView(APIView):
    """Logout User"""

    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        """Delete the user's token, if it exists, to log them out"""
        token = getattr(request.user, "auth_token", None)
        if token:
            request.user.auth_token.delete()
            data = {
                "message": "You have successfully logged out.",
            }
        else:
            data = {"message": "Goodbye"}

        return Response(data, status=status.HTTP_200_OK)
