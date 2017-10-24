from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib.auth import (
    get_user_model,
    login as django_login,
    logout as django_logout,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import SignupForm, LoginForm

User = get_user_model()


def login(request):
    # GET파라미터의 'next'값을 사용하도록 수정
    next_path = request.GET.get('next')

    # POST요청 (Form submit)의 경우
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            if next_path:
                return redirect(next_path)
            return redirect('post:post_list')
    else:
        # GET요청에서는 Form을 보여줌
        form = LoginForm()
    context = {
        'login_form': form,
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    if request.method == 'POST':
        # 데이터가 binding된 SignupForm인스턴스를 생성
        form = SignupForm(request.POST, request.FILES)
        # 해당 form이 자신의 필드에 유효한 데이터를 가지고 있는지 유효성 검사
        if form.is_valid():
            user = form.save()
            # 회원가입이 완료된 후 해당 유저를 login시킴
            django_login(request, user)
            return redirect('post:post_list')

    # GET요청시 SignupForm인스턴스를 form변수에 할당, context에 같은 키/값으로 전달
    else:
        form = SignupForm()
    context = {
        'signup_form': form,
    }
    return render(request, 'member/signup.html', context)


@login_required
def profile(request):
    return HttpResponse(f'User profile page {request.user}')


def facebook_login(request):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        type: str
        user_id: str

    class UserInfo:
        def __init__(self, data):
            self.id = data['id']
            self.email = data.get('email', '')
            self.url_picture = data['picture']['data']['url']

    app_id = settings.FACEBOOK_APP_ID
    app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
    app_access_token = f'{app_id}|{app_secret_code}'
    code = request.GET.get('code')

    def get_access_token_info(code_value):
        # 사용자가 페이스북에 로그인하기 위한 링크에 있던 'redirect_uri' GET파라미터의 값과 동일한 값
        redirect_uri = '{scheme}://{host}{relative_url}'.format(
            scheme=request.scheme,
            host=request.META['HTTP_HOST'],
            relative_url=reverse('member:facebook_login'),
        )
        print('redirect_uri:', redirect_uri)
        # 액세스 토큰을 요청하기 위한 엔드포인트
        url_access_token = 'https://graph.facebook.com/v2.10/oauth/access_token'
        # 액세스 토큰 요청의 GET파라미터 목록
        params_access_token = {
            'client_id': app_id,
            'redirect_uri': redirect_uri,
            'client_secret': app_secret_code,
            'code': code_value,
        }
        # 요청 후 결과를 받아옴
        response = requests.get(url_access_token, params_access_token)
        # 결과는 JSON형식의 텍스트이므로 아래와 같이 사용
        # json.loads(response.content) 와 같음

        # AccessTokenInfo(access_token=response.json()['access_token'],
        #    'token_type'=response.json()['token_type.....
        return AccessTokenInfo(**response.json())

    def get_debug_token_info(token):
        url_debug_token = 'https://graph.facebook.com/debug_token'
        params_debug_token = {
            'input_token': token,
            'access_token': app_access_token,
        }
        response = requests.get(url_debug_token, params_debug_token)
        return DebugTokenInfo(**response.json()['data'])

    # 전달받은 code값으로 AccessTokenInfo namedtuple을 반환
    access_token_info = get_access_token_info(code)
    # namedtuple에서 'access_token'속성의 값을 가져옴
    access_token = access_token_info.access_token
    # DebugTokenInfo 가져오기
    debug_token_info = get_debug_token_info(access_token)

    # 유저정보 가져오기
    user_info_fields = [
        'id',
        'name',
        'picture',
        'email',
    ]
    url_graph_user_info = 'https://graph.facebook.com/me'
    params_graph_user_info = {
        'fields': ','.join(user_info_fields),
        'access_token': access_token,
    }
    response = requests.get(url_graph_user_info, params_graph_user_info)
    result = response.json()
    user_info = UserInfo(data=result)

    # 페이스북으로 가입한 유저의 username
    #   fb_<facebook_user_id>
    username = f'fb_{user_info.id}'
    # 위 username에 해당하는 User가 있는지 검사
    if User.objects.filter(username=username).exists():
        # 있으면 user에 해당 유저를 할당
        user = User.objects.get(username=username)
    else:
        # 없으면 user에 새로 만든 User를 할당
        user = User.objects.create_user(
            user_type=User.USER_TYPE_FACEBOOK,
            username=username,
            age=0
        )
    # user를 로그인시키고 post_list페이지로 이동
    django_login(request, user)
    return redirect('post:post_list')
