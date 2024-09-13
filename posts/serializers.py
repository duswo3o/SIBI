from rest_framework import serializers
from .models import Post, Comment, Hashtag


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
            "hashtags",
        ]

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = [
            "name",
        ]

# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = [
#             "id",
#             "content",
#             "created_at",
#         ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at"]
        read_only_fields = ["id", "author", "created_at"]
