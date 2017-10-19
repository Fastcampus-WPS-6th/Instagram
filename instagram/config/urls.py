"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from post import views as post_views
from member import views as member_views

urlpatterns = [
    # Django admin
    url(r'^admin/', admin.site.urls),

    # Post application
    url(r'^post/$',
        post_views.post_list,
        name='post_list'),
    url(r'^post/create/$',
        post_views.post_create,
        name='post_create'),
    url(r'^post/(?P<post_pk>\d+)/$',
        post_views.post_detail,
        name='post_detail'),
    url(r'^post/(?P<post_pk>\d+)/comment/create/$',
        post_views.comment_create,
        name='comment_create'),

    # Member application
    url(r'^member/signup/$',
        member_views.signup,
        name='signup'),
    url(r'^member/login/$',
        member_views.login,
        name='login'),
    url(r'^member/logout/$',
        member_views.logout,
        name='logout'),
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
