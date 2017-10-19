from django.db import models


class Post(models.Model):
    photo = models.ImageField(upload_to='post')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 가장 나중에 달린 Comment가 가장 나중에 오도록 ordering설정
        ordering = ['created_at']
