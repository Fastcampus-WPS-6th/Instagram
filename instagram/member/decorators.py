"""
이 데코레이터를 사용한 뷰는
request.user가 인증되어있지 않으면
member:login뷰로 이동

request.META['HTTP_REFERER']
    현재 요청 이전에 어디에 있었는지
"""
from functools import wraps
from urllib.parse import urlparse

from django.shortcuts import redirect
from django.urls import reverse


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view_func(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated:
            referer = urlparse(request.META['HTTP_REFERER']).path
            url = '{base_url}?next={referer}'.format(
                base_url=reverse('member:login'),
                referer=referer)
            return redirect(url)
        return view_func(*args, **kwargs)

    return wrapped_view_func
