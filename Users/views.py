# Users/views.py
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from .models import CustomUser, UserDetails
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserDetailsSerializer,
    UserUpdateSerializer
)

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout

from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication

from django.http import JsonResponse
from django.urls import get_resolver, URLResolver, URLPattern


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = CustomUser.objects.filter(email=email).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({'token': token.key, 'email': user.email, 'user_id': user.id}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'detail': 'User registered successfully.'}, status=status.HTTP_201_CREATED)


class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    # Add any additional configurations or filters as needed


class UserLogoutView(APIView):
    def get(self, request, *args, **kwargs):
        if request.auth:  # Check if authentication token exists
            request.auth.delete()  # Delete the authentication token
        logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)


class UserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


def get_all_urls(urlpatterns, prefix=''):
    url_list = []
    for pattern in urlpatterns:
        if isinstance(pattern, tuple(get_resolver(None).url_patterns)):
            url_list.append(prefix + str(pattern.pattern))
        elif isinstance(pattern, list):
            url_list.extend(get_all_urls(pattern, prefix))
    return url_list

def get_all_urls(urlpatterns, prefix=''):
    url_list = []
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            url_list.append(prefix + str(pattern.pattern))
        elif isinstance(pattern, URLResolver):
            url_list.extend(get_all_urls(pattern.url_patterns,prefix + str(pattern.pattern)))
    return url_list


def all_urls(request):
    all_urls_list = get_all_urls(get_resolver(None).url_patterns)
    return JsonResponse({'urls': all_urls_list})


# def all_urls(request):
#     specific_urls = [
#         'path(\'\', include(router.urls))',
#         'path(\'register/\', UserRegistrationView.as_view(), name=\'user-register\')',
#         'path(\'login/\', UserLoginView.as_view(), name=\'user-login\')',
#         'path(\'logout/\', UserLogoutView.as_view(), name=\'user-logout\')',
#         'path(\'update/\', UserUpdateView.as_view(), name=\'user-update\')',
#         'path(\'all_urls/\', all_urls, name=\'all-urls\')',
#     ]
#     return JsonResponse({'urls': specific_urls})
