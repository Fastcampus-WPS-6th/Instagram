# PostList를 리턴하는 APIView를 만드세요
# 근데 APIView를 상속받도록
# Serializer도 생성 (serializers.py)
# get요청만 응답
from rest_framework import mixins, generics

from .models import Post
from .serializers import PostSerializer


class PostList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
