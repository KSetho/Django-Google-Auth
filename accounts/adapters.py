from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    
    def get_login_redirect_url(self, request):
        """
        Returns the default URL to redirect to after logging in.
        """
        return '/auth/success/'
    
    def get_signup_redirect_url(self, request):
        """
        Returns the default URL to redirect to after signing up.
        """
        return '/auth/success/'
