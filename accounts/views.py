from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .validators import validate_signup


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
