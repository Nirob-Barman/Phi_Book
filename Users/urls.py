# Users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, UserLoginView, UserDetailsViewSet, UserLogoutView, UserUpdateView, all_urls

router = DefaultRouter()
router.register('user_details', UserDetailsViewSet, basename='user-details')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('all_urls/', all_urls, name='all-urls'),
    # Add other URLs as needed
]
