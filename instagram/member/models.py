from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.db import models
from rest_framework.authtoken.models import Token


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=30, *args, **kwargs)

    def create_facebook_user(self, facebook_user_id):
        # Facebook type의 유저를 생성
        pass


class User(AbstractUser):
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_DJANGO = 'd'
    CHOICES_USER_TYPE = (
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_DJANGO, 'Django'),
    )
    user_type = models.CharField(
        max_length=1,
        choices=CHOICES_USER_TYPE
    )
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='user',
        blank=True)
    age = models.IntegerField('나이')
    like_posts = models.ManyToManyField(
        'post.Post',
        related_name='like_users',
        blank=True,
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

    @property
    def token(self):
        return Token.objects.get_or_create(user=self)[0].key

    def follow_toggle(self, user):
        # 1. 주어진 user가 User객체인지 확인
        #    아니면 raise ValueError()
        # 2. 주어진 user를 follow하고 있으면 해제
        #    안 하고 있으면 follow함
        if not isinstance(user, User):
            raise ValueError('"user" argument must be User instance!')

        relation, relation_created = self.following_user_relations.get_or_create(to_user=user)
        if relation_created:
            return True
        relation.delete()
        return False

        # if user in self.following_users.all():
        #     Relation.objects.filter(
        #         from_user=self,
        #         to_user=user,
        #     ).delete()
        # else:
        #     # Relation중개모델을 직접 사용하는 방법
        #     Relation.objects.create(
        #         from_user=self,
        #         to_user=user,
        #     )
        #     # Relation에 대한역참조 매니저를 사용하는 방법
        #     self.following_user_relations.create(to_user=user)


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
