from rest_framework import serializers

from member.serializers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'photo',
            'created_at',
        )
