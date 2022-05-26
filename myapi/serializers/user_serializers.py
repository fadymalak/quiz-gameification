from datetime import datetime
from django.forms import ValidationError
from rest_framework import serializers
from myapi.models import User
from myapi.utils import check_unique
from dataclasses import dataclass
from serpyco import Serializer
from myapi.serializers.serial import ID , CreatedAt
@dataclass
class Username(ID):
    username: str

@dataclass
class User(Username,CreatedAt):
    full_name : str
    picture : str
    email : str
    first_name : str
    last_name : str
    bio :str
    private : bool

UsernameSerial = Serializer(Username)
UserSerial = Serializer(User)

class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name="user-detail", source="id", read_only=True
    )
#    RFC7231 - section 6.3.2 Location header contain url for new resources
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "url"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        """
        validate username field
        """
        if not check_unique("username", value):
            raise serializers.ValidationError("username already exists")
        return value

    def validate_email(self, value):
        """
        validate email field
        """
        if not check_unique("email", value):
            raise serializers.ValidationError("phone already exists")
        return value

    def validate_phone(self, value):
        """
        validate phone field
        """
        if not check_unique("phone", value):
            raise serializers.ValidationError("phone already exists")
        return value


class UserDetailsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="full_name", read_only=True)

    class Meta:
        model = User
        fields = "__all__"
        depth = 1
        extra_kwargs = {"password": {"write_only": True}}
# 