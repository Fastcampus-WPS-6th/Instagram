from django.conf.urls import url, include
from django.contrib import admin

from .. import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.index, name='index'),
    url(r'^post/', include('post.urls', namespace='post')),
    url(r'^member/', include('member.urls', namespace='member')),
]
