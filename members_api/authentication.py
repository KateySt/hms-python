import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()
JWT_SETTINGS = getattr(settings, "SIMPLE_JWT", {})


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.META.get("HTTP_AUTHORIZATION")

        if not header:
            return None
        try:
            prefix, token = header.split()
        except ValueError:
            raise AuthenticationFailed("Invalid header")

        if prefix not in JWT_SETTINGS.get("AUTH_HEADER_TYPES", ("Bearer",)):
            return None

        if cache.get(f"blacklist_{token}"):
            raise AuthenticationFailed("Token blacklisted")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        if not payload.get("token_type") == "access":
            raise AuthenticationFailed("Invalid token type")

        try:
            user = User.objects.get(
                id=payload["id"], phone=payload["phone"], is_active=True
            )
        except User.DoesNotExist:
            raise AuthenticationFailed("User does not exist")

        return (user, token)
