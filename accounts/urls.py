from django.urls import path
from . import views

urlpatterns = [
    path('google/', views.google_auth, name='google_auth'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('refresh/', views.refresh_token, name='refresh_token'),
    path('test/', views.test_endpoint, name='test_endpoint'),
]
