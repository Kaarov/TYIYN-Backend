from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "bio", "language")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "language",
            "password",
            "password2",
            "fcm_token",
        )
        extra_kwargs = {"username": {"required": True}, "email": {"required": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        language = validated_data.pop("language", None)
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            language=language,
            fcm_token=validated_data["fcm_token"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, attrs):
        user = self.context["user"]
        if not user.check_password(attrs):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return attrs

    def update_password(self, validated_data):
        user = self.context["user"]
        new_pass = validated_data["password"]
        user.set_password(new_pass)
        user.save()
