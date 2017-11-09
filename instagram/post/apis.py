# PostList를 리턴하는 APIView를 만드세요
# 근데 APIView를 상속받도록
# Serializer도 생성 (serializers.py)
# get요청만 응답
from rest_framework import mixins, generics

from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
