from .models import UserLoginRecord, User
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator


class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "password": {"required": True},
            "mobile_number": {"required": True},
        }

    def validate_email(self, value):
        validate_email(value)
        return value

    def validate_password(self, value):
        try:
            validate_password(value)  # Validate standard Django password requirements
            regex = [
                "[A-Z]+",  # At least one uppercase letter
                "[a-z]+",  # At least one lowercase letter
                "[0-9]+",  # At least one digit
                "[\W]+",  # At least one non-alphanumeric character
            ]
            # Check if the password contains at least one of each type
            if not all(
                [
                    any(char.isdigit() for char in value),
                    any(char.isupper() for char in value),
                    any(char.islower() for char in value),
                    any(not char.isalnum() for char in value),
                ]
            ):
                raise serializers.ValidationError(
                    "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one non-alphanumeric character."
                )
        except serializers.ValidationError:
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one non-alphanumeric character."
            )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("The two password fields must match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2", None)
        validated_data["username"] = validated_data["email"]
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLoginRecord
        fields = ["id", "user", "login_time", "logout_time"]
        read_only_fields = ["login_time", "logout_time"]
