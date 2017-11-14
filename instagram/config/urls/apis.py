from django.conf.urls import url

from member.apis import Login, Signup, FacebookLogin
from post.apis import PostList

urlpatterns = [
    url(r'^post/$', PostList.as_view(), name='api-post'),
    url(r'^member/login/$', Login.as_view(), name='api-login'),
    url(r'^member/signup/$', Signup.as_view(), name='api-signup'),
    url(r'^member/facebook-login/$', FacebookLogin.as_view(), name='api-facebook-login'),
]
