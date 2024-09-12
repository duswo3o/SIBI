from django.urls import path
from .views import PostListAPIView, PostCreateAPIView

app_name = "posts"
urlpatterns = [
    path("", PostListAPIView.as_view(), name="post_list"),
    path("create/", PostCreateAPIView.as_view(), name="post_create"),
]
