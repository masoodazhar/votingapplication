from django.shortcuts import render, redirect
from . forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import login

# for API Usage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from . serializers import LoginSerializer, RegisterSerializer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import generics


# Backend registeration function
def index(request):

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("dashboard:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:   
        form = UserRegistrationForm()

    return render (request, "registration/register.html", context={"form":form})

# frontend Login Class API
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)})
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# frontend Register Class API
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)

        try:
            validate_email(email)
        except ValidationError:
            return Response({'detail': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)

        if not username or len(username) < 4:
            return Response({'detail': 'Username should be at least 4 characters long'}, status=status.HTTP_400_BAD_REQUEST)

        if not password or len(password) < 6:
            return Response({'detail': 'Password should be at least 6 characters long'}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({'detail': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'User registration successful'})