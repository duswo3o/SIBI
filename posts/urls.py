from django.urls import path
from .views import PostDeleteAPIView, PostUpdateAPIView

app_name = 'posts'
urlpatterns = [
    path('posts/<int:pk>/', PostDeleteAPIView.as_view(), name='post_delete'),
    path('posts/<int:pk>/', PostUpdateAPIView.as_view(), name='post_update'),

]