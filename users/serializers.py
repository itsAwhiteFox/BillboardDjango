from rest_framework import serializers
from .models import CustomUser, UserImages
from django.contrib.auth import authenticate


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id","firstName", "lastName", "email", "phone", "is_active","company", "is_staff")

class CustomUserShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email")

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImages
        fields = '__all__'
