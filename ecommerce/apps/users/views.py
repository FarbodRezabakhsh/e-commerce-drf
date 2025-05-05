from django.shortcuts import render
from .serializers import RegisterSerializer, ProfileSerializers
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Create your views here.

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

LoginView = TokenObtainPairView
RefreshView = TokenRefreshView