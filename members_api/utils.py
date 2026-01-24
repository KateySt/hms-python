from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings

JWT_SETTINGS = getattr(settings, "SIMPLE_JWT", {})
ACCESS_TOKEN_LIFETIME = JWT_SETTINGS.get("ACCESS_TOKEN_LIFETIME", timedelta(minutes=5))
REFRESH_TOKEN_LIFETIME = JWT_SETTINGS.get("REFRESH_TOKEN_LIFETIME", timedelta(days=1))


def create_access_token(user):
    return jwt.encode(
        {
            "id": user.id,
            "phone": user.phone,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
            "exp": datetime.now(timezone.utc) + ACCESS_TOKEN_LIFETIME,
            "iat": datetime.now(timezone.utc),
            "token_type": "access",
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )


def create_refresh_token(user):
    return jwt.encode(
        {
            "id": user.id,
            "exp": datetime.now(timezone.utc) + REFRESH_TOKEN_LIFETIME,
            "iat": datetime.now(timezone.utc),
            "token_type": "refresh",
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )
