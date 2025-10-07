from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']


class SocialAccountSerializer(serializers.ModelSerializer):
    """Serializer for SocialAccount model"""
    
    class Meta:
        model = SocialAccount
        fields = ['provider', 'uid', 'date_joined']
        read_only_fields = ['provider', 'uid', 'date_joined']


class GoogleAuthSerializer(serializers.Serializer):
    """Serializer for Google authentication request"""
    id_token = serializers.CharField(required=True)


class RefreshTokenSerializer(serializers.Serializer):
    """Serializer for token refresh request"""
    refresh = serializers.CharField(required=True)


class LogoutSerializer(serializers.Serializer):
    """Serializer for logout request"""
    refresh_token = serializers.CharField(required=False)
