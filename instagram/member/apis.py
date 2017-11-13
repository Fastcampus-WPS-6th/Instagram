from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, SignupSerializer

User = get_user_model()


class Login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(
            username=username,
            password=password,
        )
        if user:
            # 'user'키에 다른 dict로 유저에 대한 모든 정보를 보내줌
            token, token_created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user': UserSerializer(user).data
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {
            'message': 'Invalid credentials'
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class Signup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py에
# class FrontFacebookLogin(View):
# URL: /member/front-facebook-login/

# Facebook쪽 앱 설정에서 리다이렉트 URI에 위 URL을 추가

# facebook_login()뷰가 하던 일을 대부분 동일하게 하며, 마지막 결과로
# JsonResponse로 {'access_token': <액세스 토큰값>, 'facebook_user_id': <해당유저의 app에 대한 페이스북 ID(고유값)}
# 을 리턴하도록 함