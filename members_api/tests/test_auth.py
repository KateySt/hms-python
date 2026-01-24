import uuid

import jwt
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIClient, APIRequestFactory

from members_api.authentication import JWTAuthentication
from members_api.factories import UserFactory, InactiveUserFactory
from members_api.utils import create_refresh_token

pytestmark = pytest.mark.django_db
User = get_user_model()


class TestLoginView:
    login_url = reverse("token")
    phone = "+380671234567"
    password = "Test123!"

    def test_login_success(self, client: APIClient):
        user = UserFactory(password=self.password, phone=self.phone)

        response = client.post(
            self.login_url,
            {
                "phone": self.phone,
                "password": self.password,
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

        payload = jwt.decode(
            response.json()["access_token"], settings.SECRET_KEY, algorithms=["HS256"]
        )
        assert payload["id"] == user.id

    def test_login_invalid_credentials(self, client: APIClient):
        UserFactory(password=self.password, phone=self.phone)
        response = client.post(
            self.login_url,
            {
                "phone": self.phone,
                "password": "wrongPass",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"error": "Invalid credentials"}

    def test_login_invalid_phone(self, client: APIClient):
        UserFactory(password=self.password, phone=self.phone)
        response = client.post(
            self.login_url,
            {
                "phone": "wrongPhone",
                "password": self.password,
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"error": "Invalid credentials"}


class TestRefreshTokenView:
    refresh_token_url = reverse("refresh")
    wrong_refresh_token = "wrongToken"
    phone = "+380671234567"
    password = "Test123!"

    def test_refresh_token_success(self, client: APIClient):
        user = UserFactory(password=self.password, phone=self.phone)
        response = client.post(
            self.refresh_token_url,
            {
                "refresh_token": create_refresh_token(user),
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()

    def test_refresh_token_invalid_token(self, client: APIClient):
        UserFactory(password=self.password, phone=self.phone)
        response = client.post(
            self.refresh_token_url,
            {
                "refresh_token": self.wrong_refresh_token,
            },
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Invalid token"}


class TestJWTAuthentication:
    factory = APIRequestFactory()
    auth = JWTAuthentication()
    password = "Test123!"
    phone = "+380671234567"
    url = "members"

    def create_user_and_token(self, token_type="access", is_active=True):
        user = (
            UserFactory(phone=self.phone, password=self.password)
            if is_active
            else InactiveUserFactory(phone=self.phone, password=self.password)
        )
        payload = {
            "id": user.id,
            "phone": user.phone,
            "token_type": token_type,
            "jti": str(uuid.uuid4()),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return user, token

    def test_no_header(self):
        request = self.factory.get(self.url)
        assert self.auth.authenticate(request) is None

    def test_invalid_header_format(self):
        request = self.factory.get(
            self.url, HTTP_AUTHORIZATION="BearerTokenWithoutSpace"
        )
        with pytest.raises(AuthenticationFailed, match="Invalid header"):
            self.auth.authenticate(request)

    def test_invalid_prefix(self):
        user, token = self.create_user_and_token()
        request = self.factory.get(self.url, HTTP_AUTHORIZATION=f"Token {token}")
        assert self.auth.authenticate(request) is None

    def test_blacklisted_token(self):
        user, token = self.create_user_and_token()
        cache.set(f"blacklist_{token}", True)
        request = self.factory.get(self.url, HTTP_AUTHORIZATION=f"Bearer {token}")
        with pytest.raises(AuthenticationFailed, match="Token blacklisted"):
            self.auth.authenticate(request)

    def test_expired_token(self):
        from jwt import encode

        user, _ = self.create_user_and_token()
        payload = {"id": user.id, "phone": user.phone, "token_type": "access", "exp": 0}
        token = encode(payload, settings.SECRET_KEY, algorithm="HS256")
        request = self.factory.get(self.url, HTTP_AUTHORIZATION=f"Bearer {token}")
        with pytest.raises(AuthenticationFailed, match="Token has expired"):
            self.auth.authenticate(request)

    def test_invalid_token(self):
        request = self.factory.get(
            self.url, HTTP_AUTHORIZATION="Bearer invalid.token.here"
        )
        with pytest.raises(AuthenticationFailed, match="Invalid token"):
            self.auth.authenticate(request)

    def test_invalid_token_type(self):
        user, token = self.create_user_and_token(token_type="refresh")
        request = self.factory.get(self.url, HTTP_AUTHORIZATION=f"Bearer {token}")
        with pytest.raises(AuthenticationFailed, match="Invalid token type"):
            self.auth.authenticate(request)

    def test_user_does_not_exist(self):
        user, token = self.create_user_and_token()
        user.delete()
        request = self.factory.get(self.url, HTTP_AUTHORIZATION=f"Bearer {token}")
        with pytest.raises(AuthenticationFailed, match="User does not exist"):
            self.auth.authenticate(request)

    def test_user_not_active(self):
        user, token = self.create_user_and_token(is_active=False)
        request = self.factory.get(self.url, HTTP_AUTHORIZATION=f"Bearer {token}")
        with pytest.raises(AuthenticationFailed, match="User does not exist"):
            self.auth.authenticate(request)

    def test_successful_authentication(self):
        user, token = self.create_user_and_token()
        request = self.factory.get(self.url, HTTP_AUTHORIZATION=f"Bearer {token}")
        authenticated_user, auth_token = self.auth.authenticate(request)
        assert authenticated_user.id == user.id
        assert auth_token == token
