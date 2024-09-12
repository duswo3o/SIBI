from django.urls import path
from .views import PostListAPIView

app_name = "posts"
urlpatterns = [
    path("", PostListAPIView.as_view(), name="post_list"),
]
