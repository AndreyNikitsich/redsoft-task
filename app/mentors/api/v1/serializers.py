from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

UserModel = get_user_model()


class CustomObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "username"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["username", "password", "email", "phone"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(UserRegistrationSerializer):
    class Meta:
        model = UserModel
        fields = ["username", "email", "role", "phone", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        return super(UserUpdateSerializer, self).update(instance, validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    students = UserShortSerializer(many=True, read_only=True)
    mentors = UserShortSerializer(many=True, read_only=True)

    class Meta:
        model = UserModel
        fields = ["id", "username", "email", "role", "phone", "students", "mentors"]
