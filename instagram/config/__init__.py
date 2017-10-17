"""
member앱을 생성

1. templates/member/signup.html
    input 2개를 구현
    name은 각각 username, password

2. views.py에
    def signup(request):
        POST요청일 때
            request.POST로 전달된 username, password값을 이용해
            새 유저를 생성 (create_user()메서드를 사용)
            그리고 만든 유저의 username과 password를 HttpResponse로 리턴
        GET요청일 때
            위에서 작성한 템플릿을 보여줌

3. 사용하는 URL은
    /member/signup/

4. 위의 input들을 member/forms.py의 SignupForm으로 구성


# 숙제
https://docs.djangoproject.com/en/1.11/topics/auth/default/#authentication-in-web-requests
1. def login(request):
    이 뷰에서 사용자 로그인을 시킴

2. base.html에 사용자의 로그인 여부를 출력, 로그인 되어있지 않으면 '로그인하기'버튼을 구현
3. 로그인하기 버튼을 누르면 위의 login()뷰를 출력
4. 로그인되어있으면 '로그아웃'버튼을 보여주고, 누를시 사용자 로그아웃 처리
"""
