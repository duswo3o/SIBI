from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.UserCreateAPIView().as_view(), name="signup"),
    path("signin/", views.UserSigninAPIView.as_view()),
]
