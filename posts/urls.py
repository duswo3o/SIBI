from django.urls import path
from .views import PostListAPIView, PostCreateAPIView, PostDeleteAPIView, PostUpdateAPIView


app_name = "posts"
urlpatterns = [
    path("", PostListAPIView.as_view(), name="post_list"),
    path("create/", PostCreateAPIView.as_view(), name="post_create"),
    path('<int:pk>/', PostDeleteAPIView.as_view(), name='post_delete'),
]

