from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class Login(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        username = request.data['username']
        password = request.data['password']

        # 전달받은 username, password값으로
        # authenticate실행
        user = authenticate(
            username=username,
            password=password,
        )
        # user가 존재할 경우 (authenticate에 성공)
        if user:
            token, token_created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
            }
            return Response(data, status=status.HTTP_200_OK)
        # 인증에 실패한 경우
        else:
            data = {
                'username': username,
                'password': password,
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        # 전달받은 데이터: request.data를 사용
        # URL: /api/member/login/
        # 1. username/password를 받음
        # 2. authenticate를 이용해 사용자 인증
        # 3. 인증된 사용자에 해당하는 토큰을 생성
        # 4. 사용자 정보와 token.key값을 Response로 돌려줌
