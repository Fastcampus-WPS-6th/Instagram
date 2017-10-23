from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.db import models


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=30, *args, **kwargs)


class User(AbstractUser):
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='user',
        blank=True)
    age = models.IntegerField('나이')
    like_posts = models.ManyToManyField(
        'post.Post',
        verbose_name='좋아요 누른 포스트 목록'
    )
    # 내가 팔로우하고 있는 유저 목록
    #
    # 내가 A를 follow 한다
    #   나는 A의 follower이며
    #   A는 나의 followed_user이다

    # 나를 follow하고 있는 사람 목록은
    #   followers
    # 내가 follow하고 있는 사람 목록은
    #   followed_users
    following_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Relation',
        related_name='followers',
    )

    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'


class Relation(models.Model):
    # User의 follow목록을 가질 수 있도록
    # MTM에 대한 중개모델을 구성
    # from_user, to_user, created_at으로 3개의 필드를 사용
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_user_relations',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower_relations',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Relation (' \
               f'from: {self.from_user.username}, ' \
               f'to: {self.to_user.username})'
