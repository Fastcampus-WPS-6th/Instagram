from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # 조건에 objects의 query를 이용해서 중복을 막기
        # 이미 해당 User가 존재하는지 검사
        if username and password:
            user = User.objects.create_user(
                username=username,
                password=password
            )
            return HttpResponse(f'{user.username}, {user.password}')

    return render(request, 'member/signup.html')
