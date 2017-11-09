import io
from random import randint

from django.contrib.auth import get_user_model
from django.core.files import File
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APILiveServerTestCase

from post.apis import PostList
from post.models import Post

User = get_user_model()


class PostListViewTest(APILiveServerTestCase):
    URL_API_POST_LIST_NAME = 'api-post'
    URL_API_POST_LIST = '/api/post/'
    VIEW_CLASS = PostList

    def test_post_list_url_name_reverse(self):
        url = reverse(self.URL_API_POST_LIST_NAME)
        self.assertEqual(url, self.URL_API_POST_LIST)

    def test_post_list_url_resolve_view_class(self):
        # /api/post/에 매칭되는 ResolverMatch객체를 가져옴
        resolver_match = resolve(self.URL_API_POST_LIST)
        # ResolverMatch의 url_name이 'api-post'(self.URL_API_POST_LIST_NAME)인지 확인
        self.assertEqual(
            resolver_match.url_name,
            self.URL_API_POST_LIST_NAME)
        # ResolverMatch의 func이 PostList(self.VIEW_CLASS)인지 확인
        self.assertEqual(
            resolver_match.func.view_class,
            self.VIEW_CLASS)

    def test_get_post_list(self):
        user = User.objects.create_user(username='dummy', age=0)
        # 0이상 20이하의 임의의 숫자 지정
        num = randint(0, 20)
        # num개수만큼 Post생성, author를 지정해줌
        for i in range(num):
            Post.objects.create(
                author=user,
                photo=File(io.BytesIO()),
            )

        url = reverse(self.URL_API_POST_LIST_NAME)
        # post_list에 GET요청
        response = self.client.get(url)
        # status code가 200인지 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # objects.count결과가 num과 같은지 확인
        self.assertEqual(Post.objects.count(), num)
        # response로 돌아온 JSON리스트의 길이가 num과 같은지 확인
        self.assertEqual(len(response.data), num)

        
