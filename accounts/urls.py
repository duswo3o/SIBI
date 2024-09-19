from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.UserCreateAPIView().as_view(), name="signup"),
    path("signin/", views.UserSigninAPIView.as_view()),
    path("signout/", views.UserSignoutAPIView.as_view(), name="signout"),
    path(
        "password-reset/", views.PasswordResetAPIView.as_view(), name="password-reset"
    ),
    path("<str:username>/", views.ProfileDetailAPIView.as_view(), name="profile"),
    path("<str:username>/follow/", views.ProfileFollowAPIView.as_view(), name="follow"),
]
