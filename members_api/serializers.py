from django.contrib.auth import get_user_model
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from courses_app.models import Course

User = get_user_model()


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["id", "updated_at", "created_at"]


class MemberSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    courses_id = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Course.objects.all(), allow_null=True, write_only=True
    )
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "date_of_birth",
            "gender",
            "language",
            "color",
            "full_name",
            "courses",
            "courses_id",
        ]
        read_only_fields = ["id"]

    @extend_schema_field(serializers.CharField())
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class JWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "members_api.authentication.JWTAuthentication"
    name = "Bearer"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
