import openai
from django.db.models import Count
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Comment, Hashtag, Like, UrlContent, Headline
from .serializers import (
    PostSerializer,
    PostCreateSerializer,
    CommentSerializer,
    HashtagSerializer,
    LikeSerializer,
    CrawlingSerializer,
)
from .validators import validate_hashtags
from .crawling import get_content
from openai_test import summery_article

from django.shortcuts import get_object_or_404
from django.contrib.sites import requests

from SIBI_NEWS.config import OPENAI_API_KEY
import requests

openai.api_key = OPENAI_API_KEY


class PostListAPIView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.annotate(like_count=Count("likes")).order_by("-like_count")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        is_valid, valid_hashtags = validate_hashtags(request.data)

        hashtag_instances = []
        if valid_hashtags:
            for hashtag_name in valid_hashtags:
                # get_or_create로 hashtag instance 가져오거나 새로 생성
                hashtag, created = Hashtag.objects.get_or_create(name=hashtag_name)
                hashtag_instances.append(hashtag)

        post_data = request.data.copy()
        #'hashtags'를 따로 처리하기 위해 post_data에서 빼기
        post_data.pop("hashtags", None)

        # DB 저장하지 말고 post instance 생성
        post_serializer = PostCreateSerializer(data=post_data)

        if post_serializer.is_valid(raise_exception=True):
            # author 정하고 post instance 저장
            post = post_serializer.save(author=request.user)

            # 만들어진 post에 hashtags를 더해주기
            post.hashtags.set(hashtag_instances)
            post.save()

            # 생성된 Post 인스턴스를 serialize해서 Response 데이터를 만듦
            post_serializer = PostCreateSerializer(post)

        return Response(post_serializer.data, status=status.HTTP_201_CREATED)


class PostDeleteUpdateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def delete(self, request, pk):
        # pk로 게시글 가져오기
        post = get_object_or_404(Post, pk=pk)

        # 요청자가 작성자인지 확인 추후 추가예정
        if post.author != request.user:
            return Response(
                {"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        # 게시글 삭제
        post.delete()

        return Response(
            {"detail": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
        )

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # 요청자가 작성자인지 확인
        if post.author != request.user:
            return Response(
                {"detail": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        # 전체 데이터를 업데이트하는 시리얼라이저
        serializer = PostSerializer(post, data=request.data)

        # 유효성 검사 후 저장
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # 요청자가 작성자인지 확인
        if post.author != request.user:
            return Response(
                {"detail": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        # 부분 데이터를 업데이트하는 시리얼라이저
        serializer = PostSerializer(post, data=request.data, partial=True)

        # 유효성 검사 후 저장
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        comments = Comment.objects.annotate(like_count=Count("like_users")).order_by(
            "-like_count"
        )
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.author != request.user:
            return Response(
                {"detail": "권한이없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response({"message": "삭제 완료."}, status=200)


class LikePostView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = LikeSerializer(data={"post": post.id, "user": request.user.id})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(post=post, user=request.user).first()

        if like:
            like.delete()
            return Response(
                {"message": "좋아요가 취소되었습니다."},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"error": "좋아요를 누르지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST
        )


class CommentLikeAPIView(APIView):
    def post(self, request, comment_pk):
        comment = get_object_or_404(Comment, id=comment_pk)
        user = get_user_model().objects.get(id=request.user.id)

        if user in comment.like_users.all():
            comment.like_users.remove(user)
            return Response({"comment": "해당 댓글에 좋아요가 취소되었습니다"})
        else:
            comment.like_users.add(user)
            return Response({"comment": "해당 댓글에 좋아요 하셨습니다"})


class CrawlingAPIView(APIView):
    def post(self, request):
        url = request.data.get("url")
        web_site = requests.get(url)

        if web_site.status_code != 200:
            return Response("찾을 수 없는 url 입니다.")

        crawling = get_content(url)
        title = crawling[0]
        content = crawling[1]
        summery_content = summery_article(content)

        # 데이터베이스에 이미 있는 url이라면 저장하지 않기
        if not UrlContent.objects.filter(url=url):
            UrlContent.objects.create(
                url=url,
                title=title,
                summery=summery_content,
            )

        serializer = CrawlingSerializer(
            data={
                "url": url,
                "title": title,
                "summery": summery_content,
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodayHeadlineAPIView(APIView):
    def get(self, request):
        headline_articles = Headline.objects.all().order_by("-id")[:5]
        serializer = CrawlingSerializer(headline_articles, many=True)
        return Response(serializer.data)
