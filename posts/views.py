
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer
from django.shortcuts import get_object_or_404



class PostListAPIView(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostCreateAPIView(APIView):

    def post(self, request):
        permission_classes = [IsAuthenticated]

        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        return Response({"detail": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

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
        return Response({"message": "삭제 완료."}, status=200)












