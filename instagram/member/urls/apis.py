from django.conf.urls import url

from .. import apis

urlpatterns = [
    # api:member:login
    url(r'^login/$', apis.Login.as_view(), name='login'),
    url(r'^signup/$', apis.Signup.as_view(), name='signup'),
    url(r'^facebook-login/$', apis.FacebookLogin.as_view(), name='facebook-login'),
]
