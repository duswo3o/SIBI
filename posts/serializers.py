from rest_framework import serializers
from .models import Post, Comment, CommentLike


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "image",
        ]

class CommentLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentLike
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at", "like_count"]
        read_only_fields = ["id", "author", "created_at"]

class DataSerializer(serializers.Serializer):
    data = serializers.ListField(child=serializers.CharField())




