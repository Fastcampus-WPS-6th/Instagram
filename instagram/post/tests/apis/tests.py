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

    @staticmethod
    def create_user(username='dummy'):
        return User.objects.create_user(username=username, age=0)

    @staticmethod
    def create_post(author=None):
        return Post.objects.create(author=author, photo=File(io.BytesIO()))

    def test_post_list_url_name_reverse(self):
        url = reverse(self.URL_API_POST_LIST_NAME)
        self.assertEqual(url, self.URL_API_POST_LIST)

    def test_post_list_url_resolve_view_class(self):
        """
        post.apis.PostList뷰에 대해
        URL reverse, resolve, 사용하고 있는 view함수가 같은지 확인
        :return:
        """
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
        """
        PostList의 GET요청 (Post목록)에 대한 테스트
        임의의 개수만큼 Post를 생성하고 해당 개수만큼 Response가 돌아오는지 확인
        :return:
        """
        user = self.create_user()
        # 0이상 20이하의 임의의 숫자 지정
        num = randint(1, 20)
        # num개수만큼 Post생성, author를 지정해줌
        for i in range(num):
            self.create_post(author=user)

        url = reverse(self.URL_API_POST_LIST_NAME)
        # post_list에 GET요청
        response = self.client.get(url)
        # status code가 200인지 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # objects.count결과가 num과 같은지 확인
        self.assertEqual(Post.objects.count(), num)
        # response로 돌아온 JSON리스트의 길이가 num과 같은지 확인
        self.assertEqual(len(response.data), num)

        # response로 돌아온 객체들이 각각 pk, author, photo, created_at키를 가지고 있는지 확인
        for i in range(num):
            cur_post_data = response.data[i]
            self.assertIn('pk', cur_post_data)
            self.assertIn('author', cur_post_data)
            self.assertIn('photo', cur_post_data)
            self.assertIn('created_at', cur_post_data)

    def test_get_post_list_exclude_author_is_none(self):
        """
        author가 None인 Post가 PostList get요청에서 제외되는지 테스트
        :return:
        """
        user = self.create_user()
        num_author_none_posts = randint(1, 10)
        num_posts = randint(11, 20)
        for i in range(num_author_none_posts):
            self.create_post()
        for i in range(num_posts):
            self.create_post(author=user)

        response = self.client.get(self.URL_API_POST_LIST)
        # author가 없는 Post개수는 response에 포함되지 않는지 확인
        self.assertEqual(len(response.data), num_posts)
