from rest_framework import serializers
from .models import Post, Comment, Hashtag, Like, UrlContent
from accounts.models import User


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ["name"]


class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "created_at",
            "updated_at",
            "image",
            "like_count",
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    # hashtags = serializers.PrimaryKeyRelatedField(queryset=Hashtag.objects.all(), many=True, required=False)
    hashtags = HashtagSerializer(many=True, read_only=True)

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


class CommentLikeCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]


class CommentSerializer(serializers.ModelSerializer):
    like_users = CommentLikeCountSerializer(many=True, read_only=True)
    like_users_count = serializers.IntegerField(
        source="like_users.count", read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "content",
            "created_at",
            "like_users",
            "like_users_count",
        ]

        read_only_fields = ("author",)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "post", "user", "created_at"]
        read_only_fields = ["id", "created_at"]


class CrawlingSerializer(serializers.Serializer):
    url = serializers.URLField()
    content = serializers.CharField()

    def create(self, validated_data):
        return UrlContent(**validated_data)
