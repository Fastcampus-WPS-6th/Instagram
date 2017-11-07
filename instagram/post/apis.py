# PostList를 리턴하는 APIView를 만드세요
# 근데 APIView를 상속받도록
# Serializer도 생성 (serializers.py)
# get요청만 응답
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
