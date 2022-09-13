from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers, validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from post_app.users.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        update_last_login(None, user)
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "date_joined", "last_login"]
        read_only_fields = ["username", "date_joined", "last_login"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Used to register users.
    """

    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            # Ensure username is required and unique
            "username": {
                "required": True,
                "validators": [
                    validators.UniqueValidator(
                        get_user_model().objects.all(),
                        message="A user with such username already exists",
                    )
                ],
            },
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance


class UserActivitySerializer(serializers.ModelSerializer):
    """
    Used to get the latest user actions.
    """

    class Meta:
        model = User
        fields = ["username", "last_login", "last_request"]
        read_only_fields = [
            "last_login",
            "last_request",
        ]
