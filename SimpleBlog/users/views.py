from datetime import datetime
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from .models import UserLoginRecord, User, TokenBlacklist
from .serializers import CustomUserSerializer, UserLoginRecordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from utils import APIResponse


@api_view(["POST"])
def register_user(request):
    try:
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(
                message="Account created successfully",
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            ).build_response()
        else:
            return APIResponse(
                error=str(serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            ).build_response()
    except Exception as e:
        return APIResponse(
            error="Failed to register user", status=status.HTTP_400_BAD_REQUEST
        ).build_response()


@api_view(["POST"])
def login_user(request):
    try:
        username = request.data.get("email")
        password = request.data.get("password")

        if username and password:
            user = User.objects.filter(username=username).first()

            if user and user.check_password(password):
                # Generate tokens for the user
                refresh = RefreshToken.for_user(user)
                UserLoginRecord.objects.create(user=user, login_time=datetime.now())
                return APIResponse(
                    "Login successful",
                    data={
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                ).build_response()
            else:
                return APIResponse(
                    error="Invalid username/email or password.",
                    status=status.HTTP_400_BAD_REQUEST,
                ).build_response()
        else:
            return APIResponse(
                error="Both username/email and password are required.",
                status=status.HTTP_400_BAD_REQUEST,
            ).build_response()
    except Exception as e:
        # Debugging: Print error message
        print(f"Error during user login: {str(e)}")
        return APIResponse(
            error="An error occurred during user login.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ).build_response()


@api_view(["POST"])
def logout_user(request):
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            user_id = token.payload.get("user_id")
            user = User.objects.get(username=user_id)

            if user:
                # Update the UserLoginRecord for logout
                latest_login = (
                    UserLoginRecord.objects.filter(user=user)
                    .order_by("-login_time")
                    .first()
                )
                if latest_login:
                    latest_login.logout_time = datetime.now()
                    latest_login.save()
                TokenBlacklist.add_to_blacklist(token["jti"])

                return APIResponse(
                    "Logged out successfully", status=status.HTTP_200_OK
                ).build_response()
            else:
                # Handle case where user does not exist
                return APIResponse(
                    error="User not found", status=status.HTTP_404_NOT_FOUND
                ).build_response()
        else:
            return APIResponse(
                error="Refresh token not provided", status=status.HTTP_400_BAD_REQUEST
            ).build_response()
    except Exception as e:
        print(f"Error during user logout: {str(e)}")
        return APIResponse(
            error="An error occurred during user logout.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ).build_response()
