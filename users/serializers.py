from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from .models import *

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('id', 'username','is_client','auth_token')
         read_only_fields = ('id', 'is_client')
    
    def get_auth_token(self, obj):
        try:
            token = Token.objects.get(user=obj)

        except Token.DoesNotExist:
            token = Token.objects.create(user=obj)

        return token.key

class EmptySerializer(serializers.Serializer):
    pass

class DesignerRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the Designer
    """
    password2 = serializers.CharField(style={"input_type":"password"}, write_only = True)
    class Meta:
        model = Designer
        fields = ('id','email', 'username', 'password','password2','phone','skills','description')

    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user:
            raise serializers.ValidationError("Username is already taken")
        return AbstractBaseUser.normalize_username(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

class ClientRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the Client
    """
    password2 = serializers.CharField(style={"input_type":"password"}, write_only = True)
    class Meta:
        model = Client
        fields = ('email', 'username', 'password','password2','phone','company_name','description')

    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user:
            raise serializers.ValidationError("Username is already taken")
        return AbstractBaseUser.normalize_username(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class ClientProfileImageUpdateSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the Client
    """
    class Meta:
        model = Client
        fields = ('profile_image')