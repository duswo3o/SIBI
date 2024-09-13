from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment, Hashtag
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer, HashtagSerializer
from .validators import validate_hashtags
from django.shortcuts import get_object_or_404



class PostListAPIView(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostCreateAPIView(APIView):

    def post(self, request):
        permission_classes = [IsAuthenticated]

        is_valid, valid_hashtags = validate_hashtags(request.data)

        print(valid_hashtags)
        if valid_hashtags:
            hashtag_instances = []
            for hashtag_name in valid_hashtags:
                # get_or_create로 hashtag instance 가져오거나 새로 생성
                hashtag, created = Hashtag.objects.get_or_create(name=hashtag_name)
                hashtag_instances.append(hashtag)
        else:
            hashtag_instances = []

        # hashtag_serializer = HashtagSerializer(data=valid_hashtags, many=True)
        # hashtag_serializer.is_valid(raise_exception=True)
        # hashtag_serializer.save()

        post_data = request.data.copy()
        # post_data 딕셔너리의 hastags에 hashtag.id 포함시키기
        post_data["hashtags"] = [hashtag.id for hashtag in hashtag_instances]
        # 유효성 체크, Post 인스턴스를 저장하기 위해 Serializer로 변환
        post_serializer = PostCreateSerializer(data=post_data)

        if post_serializer.is_valid(raise_exception=True):
            post = post_serializer.save(author=request.user)
            # 생성된 Post 인스턴스를 serialize해서 Response 데이터를 만듦
            post_serializer = PostCreateSerializer(post)

        return Response(post_serializer.data, status=status.HTTP_201_CREATED)


class PostDeleteUpdateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, pk):
        # pk로 게시글 가져오기
        post = get_object_or_404(Post, pk=pk)

        # 요청자가 작성자인지 확인 추후 추가예정
        if post.author != request.user:
            return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        # 게시글 삭제
        post.delete()

        return Response(
            {"detail": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
        )

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # 요청자가 작성자인지 확인
        if post.author != request.user:
            return Response({"detail": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

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
            return Response({"detail": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

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
        post= get_object_or_404(Post, pk=pk)
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
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)



    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.author != request.user:
            return Response({"detail": "권한이없습니다."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({"messa"
                         "ge": "삭제 완료."}, status=200)

