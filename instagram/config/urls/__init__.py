from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from . import apis, views

urlpatterns = [
    url(r'^', include(views)),
    url(r'^api/', include(apis)),
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
