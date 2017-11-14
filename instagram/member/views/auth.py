from django.conf import settings
from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
)
from django.shortcuts import redirect, render

from ..forms import LoginForm, SignupForm

__all__ = (
    'login',
    'logout',
    'signup',
)


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
