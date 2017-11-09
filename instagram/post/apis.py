# PostList를 리턴하는 APIView를 만드세요
# 근데 APIView를 상속받도록
# Serializer도 생성 (serializers.py)
# get요청만 응답
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    # api/post/
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# PostDetail APIView생성
# APIView를 사용