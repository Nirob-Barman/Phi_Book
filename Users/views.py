# Users/views.py
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from .models import CustomUser, UserDetails
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
    CustomUserSerializer
)

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.authentication import TokenAuthentication

from django.http import JsonResponse
from django.urls import path, include, get_resolver, URLResolver, URLPattern


from rest_framework.generics import UpdateAPIView


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        # email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        # user = CustomUser.objects.filter(email=email).first()
        user = CustomUser.objects.filter(username=username).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({'token': token.key, 'email': user.email, 'user_id': user.id}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# class UserRegistrationView(generics.CreateAPIView):
#     serializer_class = UserRegistrationSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Validate password and confirm_password
#         password = serializer.validated_data.get('password')
#         confirm_password = serializer.validated_data.get('confirm_password')

#         if password != confirm_password:
#             return Response({'detail': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'detail': 'User registered successfully.'}, status=status.HTTP_201_CREATED)



class UserLogoutView(APIView):
    def get(self, request, *args, **kwargs):
        if request.auth:  # Check if authentication token exists
            request.auth.delete()  # Delete the authentication token
        logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)


def get_all_urls(urlpatterns, prefix=''):
    url_list = []
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            url_list.append(prefix + str(pattern.pattern))
        elif isinstance(pattern, URLResolver):
            url_list.extend(get_all_urls(pattern.url_patterns,
                            prefix + str(pattern.pattern)))
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


class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        return self.request.user  # Returns the currently authenticated user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
