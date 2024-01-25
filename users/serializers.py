from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate

# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         username = data.get('username')
#         password = data.get('password')
#         user = authenticate(email=username, password=password)
#         if not user:
#             raise serializers.ValidationError('Incorrect credentials')
#         return user


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
        fields = ("firstName", "lastName", "email", "phone", "is_active","company", "is_staff")

class CustomUserShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email")

