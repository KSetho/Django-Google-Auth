from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
try:
    from allauth.socialaccount.models import SocialApp, SocialAccount
    from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
    from allauth.socialaccount.providers.oauth2.client import OAuth2Client
    from google.auth.transport import requests as google_requests
    from google.oauth2 import id_token
    ALLAUTH_AVAILABLE = True
except ImportError:
    ALLAUTH_AVAILABLE = False
import json

User = get_user_model()


def get_tokens_for_user(user):
    """Generate JWT tokens for a user"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class GoogleAuthView(APIView):
    """
    Authenticate user with Google OAuth2 token
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        if not ALLAUTH_AVAILABLE:
            return Response(
                {'error': 'Google authentication not properly configured'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        try:
            # Get the ID token from the request
            id_token_str = request.data.get('id_token')
            
            if not id_token_str:
                return Response(
                    {'error': 'ID token is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify the token with Google
            try:
                # Get Google client ID from settings
                google_client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
                
                # Verify the token
                idinfo = id_token.verify_oauth2_token(
                    id_token_str, 
                    google_requests.Request(), 
                    google_client_id
                )
                
                # Additional verification
                if idinfo['aud'] != google_client_id:
                    return Response(
                        {'error': 'Invalid token audience'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
            except ValueError as e:
                return Response(
                    {'error': f'Invalid token: {str(e)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Extract user information
            email = idinfo.get('email')
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            google_id = idinfo.get('sub')
            
            if not email:
                return Response(
                    {'error': 'Email not provided by Google'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if user exists
            try:
                user = User.objects.get(email=email)
                created = False
            except User.DoesNotExist:
                # Create new user
                user = User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    username=email  # Use email as username
                )
                created = True
            
            # Check if social account exists
            try:
                social_account = SocialAccount.objects.get(
                    user=user,
                    provider='google'
                )
            except SocialAccount.DoesNotExist:
                # Create social account
                social_account = SocialAccount.objects.create(
                    user=user,
                    provider='google',
                    uid=google_id,
                    extra_data=idinfo
                )
            
            # Generate JWT tokens
            tokens = get_tokens_for_user(user)
            
            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_new_user': created
                },
                'tokens': tokens
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Authentication failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    """
    Logout user by blacklisting the refresh token
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Logout failed: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(APIView):
    """
    Get current user profile
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Get social account info if exists
        social_account = None
        if ALLAUTH_AVAILABLE:
            try:
                social_account = SocialAccount.objects.get(user=user, provider='google')
            except SocialAccount.DoesNotExist:
                pass
        
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
            },
            'social_account': {
                'provider': social_account.provider if social_account else None,
                'uid': social_account.uid if social_account else None,
            } if social_account else None
        }, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    """
    Refresh JWT access token
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            return Response({
                'access': str(token.access_token)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Token refresh failed: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class TestEndpointView(APIView):
    """
    Test endpoint to verify API is working
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'message': 'API is working!',
            'allauth_available': ALLAUTH_AVAILABLE,
            'endpoints': {
                'google_auth': '/api/auth/google/',
                'logout': '/api/auth/logout/',
                'profile': '/api/auth/profile/',
                'refresh': '/api/auth/refresh/',
                'test': '/api/auth/test/'
            }
        }, status=status.HTTP_200_OK)


# Keep the function-based views as alternatives
google_auth = GoogleAuthView.as_view()
logout = LogoutView.as_view()
user_profile = UserProfileView.as_view()
refresh_token = RefreshTokenView.as_view()
test_endpoint = TestEndpointView.as_view()
