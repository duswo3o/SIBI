from django.urls import path

from .views import PostListAPIView, PostCreateAPIView, PostDeleteUpdateAPIView, CommentCreateAPIView, LikePostView

app_name = "posts"
urlpatterns = [
    path("", PostListAPIView.as_view(), name="post_list"),
    path("create/", PostCreateAPIView.as_view(), name="post_create"),
    path('<int:pk>/', PostDeleteUpdateAPIView.as_view(), name='post_update'),
    path('<int:pk>/comments/', CommentCreateAPIView.as_view(), name='comment_create'),
    path('comments/<int:pk>/', CommentCreateAPIView.as_view(), name='comment_edit_delete'),
    path('<int:pk>/like/', LikePostView.as_view(), name='post_like'),
]

