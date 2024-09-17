from django.shortcuts import redirect
import os

from json import JSONDecodeError
from django.http import JsonResponse
import requests
from rest_framework import status
from rest_framework.response import Response
from .models import User
from allauth.socialaccount.models import SocialAccount


from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view

from rest_framework_simplejwt.tokens import RefreshToken


# 구글 소셜로그인 변수 설정
state = os.environ.get("STATE")
BASE_URL = "http://127.0.0.1:8000/"
GOOGLE_CALLBACK_URI = BASE_URL + "api/accounts/google/callback/"
# print("state : ", state)


# 구글 로그인
def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}"
    )


def google_callback(request):
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    print(client_id)
    client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get("code")
    print("code : ", code)

    # 1. 받은 코드로 구글에 access token 요청
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}"
    )

    ### 1-1. json으로 변환 & 에러 부분 파싱
    token_req_json = token_req.json()
    print("==========================================")
    print(token_req_json)
    print("==========================================")
    error = token_req_json.get("error")

    ### 1-2. 에러 발생 시 종료
    if error is not None:
        return JsonResponse({"error": error}, status=status.HTTP_400_BAD_REQUEST)

    ### 1-3. 성공 시 access_token 가져오기
    access_token = token_req_json.get("access_token")

    # 2. 가져온 access_token으로 이메일값을 구글에 요청
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
    )
    email_req_status = email_req.status_code

    ### 2-1. 에러 발생 시 400 에러 반환
    if email_req_status != 200:
        return JsonResponse(
            {"err_msg": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST
        )

    ### 2-2. 성공 시 이메일 가져오기
    email_req_json = email_req.json()
    email = email_req_json.get("email")

    # return JsonResponse({'access': access_token, 'email':email})

    # 3. 전달받은 이메일, access_token, code를 바탕으로 회원가입/로그인
    try:
        # 전달받은 이메일로 등록된 유저가 있는지 탐색
        # 없다면 Exception 발생
        user = User.objects.get(email=email)
        token = RefreshToken.for_user(user)  # 자체 jwt 발급
        refresh_token = str(token)
        access_token = str(token.access_token)

        if user.is_active:
            # return JsonResponse HTTP_200_OK
            return JsonResponse({"access": access_token, "refresh": refresh_token})
        else:
            # 활성화되지 않은 회원, Exception 발생
            raise Exception("Signup Required")

    except Exception:
        # 가입이 필요한 회원
        # return JsonResponse HTTP_202_ACCEPTED
        return JsonResponse({"msg": "회원가입이 필요합니다"})


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
