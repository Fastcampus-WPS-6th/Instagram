from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


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
