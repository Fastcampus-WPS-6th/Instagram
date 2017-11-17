from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^send-sms/$', apis.SendSMS.as_view(), name='sms'),
]
