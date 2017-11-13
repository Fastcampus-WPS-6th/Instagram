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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from member.apis import Login, Signup
from post.apis import PostList
from . import views

# url모듈을 분리
#   기존 url들은 r'^' 에 매칭
#   각 애플리케이션의 apis모듈 (ex: post.apis, member.apis)는
#       r'^api/' 에 매칭되도록
#      각 애플리케이션의 urls모듈을 패키지화
#        기존 urls모듈에 있던 내용은 urls/views.py로 이동
#        apis에 있는 내용들은 urls/apis.py에 작성
# 이 urls모듈을 패키지화시키고
#   기존 URL은 urls/views.py
#   API의 URL은 urls/apis.py
#       각 파일에 urlpatterns를 정의하고
#   urls/__init__.py에서 맨 위 설명과 같은 방식이 되도록 각 모듈을 include처리

urlpatterns = [
    # Django admin
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.index, name='index'),
    url(r'^post/', include('post.urls', namespace='post')),
    url(r'^member/', include('member.urls', namespace='member')),

    url(r'^api/post/$', PostList.as_view(), name='api-post'),
    url(r'^api/member/login/$', Login.as_view(), name='api-login'),
    url(r'^api/member/signup/$', Signup.as_view(), name='api-signup'),
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
