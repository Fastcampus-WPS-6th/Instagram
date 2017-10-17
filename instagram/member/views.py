from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            # 이미 username항목이 주어진 username값으로 존재하는 User가 있는지 검사
            if User.objects.filter(username=username).exists():
                return HttpResponse(f'Username {username} is already exist')
            # username, password가 주어졌고 중복되는 User가 없다면 User생성
            user = User.objects.create_user(
                username=username,
                password=password
            )
            return HttpResponse(f'{user.username}, {user.password}')

    return render(request, 'member/signup.html')
