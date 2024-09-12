from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from .validators import validate_signup, validate_delete_account


# Create your views here.
class UserCreateAPIView(APIView):
    def post(self, request):
        is_valid, err_msg = validate_signup(request.data)
        if not is_valid:
            return Response({"error": err_msg}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(**request.data)
        serializer = UserSerializer(user)

        # 토큰 발급
        refresh = RefreshToken.for_user(user)
        # 토큰 시리얼라이저에 함게 담아서 전송
        res_data = serializer.data
        res_data["tokens"] = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        return Response(res_data, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def delete(self, request):
        user = request.user
        is_valid, err_msg = validate_delete_account(request.data, user)
        if not is_valid:
            return Response({"error": err_msg}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response(
            {"message": "계정이 삭제되었습니다."}, status=status.HTTP_200_OK
        )


class UserSigninAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {
                    "error": "유저네임과 패스워드가 일치하지 않습니다. 로그인에 실패하였습니다"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class UserSignoutAPIView(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                {"error": "refresh token이 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(
                {"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)


class ProfileDetailAPIView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, username):
        profile = get_object_or_404(User, username=username)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def put(self, request, username):
        user = get_object_or_404(User, username=username)  # 조회한 프로필

        if username != request.user.username:
            return Response(
                {"error": "수정 권한이 없는 프로필입니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = ProfileSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(APIView):
    @permission_classes([IsAuthenticated])
    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "입력한 기존 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)