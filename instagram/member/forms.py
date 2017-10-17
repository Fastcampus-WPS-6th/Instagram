from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login

User = get_user_model()


class LoginForm(forms.Form):
    """
    is_valid()에서 주어진 username/password를 사용한 authenticate실행
    성공시 login(request)메서드를 사용할 수 있음
    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # 해당하는 User가 있는지 인증
        # 인증에 성공하면 self.user변수에 User객체가 할당, 실패시 None
        self.user = authenticate(
            username=username,
            password=password
        )
        if not self.user:
            raise forms.ValidationError(
                'Invalid login credentials'
            )
        else:
            setattr(self, 'login', self._login)

    def _login(self, request):
        """
        django.contrib.auth.login(request)를 실행
        
        :param request: django.contrib.auth.login()에 주어질 HttpRequest객체
        :return: None
        """
        # Django의 Session에 해당 User정보를 추가,
        # Response에는 SessionKey값을 Set-Cookie 헤더에 담아 보냄
        # 이후 브라우저와의 요청응답에서는 로그인을 유지함
        django_login(request, self.user)


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        # required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    # clean_<field_name>
    def clean_username(self):
        data = self.cleaned_data['username']
        # 유저가 존재하면 forms.ValidationError를 발생시킴
        # 아니면 data를 리턴
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('오아ㅏ아아아아아')
        return data
