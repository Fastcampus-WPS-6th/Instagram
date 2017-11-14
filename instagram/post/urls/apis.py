from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^$', apis.PostList.as_view(), name='api-post'),
]
