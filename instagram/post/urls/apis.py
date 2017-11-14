from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^$', apis.PostList.as_view(), name='post-list'),
    url(r'^(?P<post_pk>\d+)/$', apis.PostDetail.as_view(), name='post-detail'),
    url(r'^(?P<post_pk>\d+)/like-toggle/$', apis.PostLikeToggle.as_view(), name='post-like-toggle'),
]
