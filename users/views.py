from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    LoginSerializer
)

from .permissions import IsDirector  # assume we created this


# -----------------------------
# REGISTER USER
# -----------------------------
class RegisterUserView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=201)

        return Response(serializer.errors, status=400)


# -----------------------------
# LOGIN
# -----------------------------
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })

        return Response(serializer.errors, status=400)


# -----------------------------
# CURRENT USER PROFILE
# -----------------------------
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


# -----------------------------
# LIST USERS (DIRECTOR ONLY)
# -----------------------------
class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector]

    def get(self, request):
        users = User.objects.all().order_by('-created_at')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# -----------------------------
# UPDATE USER (DIRECTOR ONLY)
# -----------------------------
class UserUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector]

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(user).data)

        return Response(serializer.errors, status=400)