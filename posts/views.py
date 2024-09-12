from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer, PostCreateSerializer
from django.shortcuts import get_object_or_404


class PostListAPIView(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostCreateAPIView(APIView):

    def post(self, request):
        # permission_classes = [IsAuthenticated]

        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      
class PostDeleteAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        # pk로 게시글 가져오기
        post = get_object_or_404(Post, pk=pk)

        # # 요청자가 작성자인지 확인 추후 추가예정
        # if post.author != request.user:
        #     return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        # 게시글 삭제
        post.delete()
        return Response({"detail": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)      
      
      
      

