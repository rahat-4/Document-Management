from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from documentio.utils import get_tokens_for_user

from ...models import User


class PublicUserRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(min_length=2, max_length=50, required=False)
    last_name = serializers.CharField(min_length=2, max_length=50, required=False)
    password = serializers.CharField(min_length=8, max_length=50, write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "gender",
            "password",
        ]

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise ValidationError({"detail": "This email already exists."})
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email").lower()
        validated_data["email"] = email

        user = User.objects.create(
            password=make_password(password),
            username=email,
            is_active=True,
            **validated_data
        )

        return user


class PublicUserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        max_length=255,
        write_only=True,
    )
    password = serializers.CharField(min_length=6, max_length=50, write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.pop("password")
        try:
            user: User = User.objects.get(email=email)
            if not user.check_password(password):
                raise ValidationError(
                    {"detail": "Authentication credentials are not correct!"}
                )

            token = get_tokens_for_user(user)
            validated_data["refresh"] = token["refresh"]
            validated_data["access"] = token["access"]

            return validated_data

        except User.DoesNotExist:
            raise ValidationError(
                {"detail": "Authentication credentials are not correct!"}
            )
