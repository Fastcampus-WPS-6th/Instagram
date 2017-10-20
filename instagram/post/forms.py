from django import forms

from .models import Post

__all__ = (
    'PostForm',
)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'photo',
        )

    def save(self, commit=True, *args, **kwargs):
        # 1. 처음으로 Post객체가 만들어지는 순간
        # 2. instance의 author필드가 비어있으면 save(commit=True)를 비허용
        #   2-1. 하지만 save(commit=False)는 허용 (나중에 author필드를 채움)
        # 3. save()에 author키워드 인수값을 전달할 수 있도록 save()메서드를 재정의

        # 새로 저장하려는 객체이다(pk값이 없음)
        # form.save(author=request.user)

        if not self.instance.pk and commit:
            author = kwargs.pop('author', None)
            if not author:
                raise ValueError('Author field is required')
            self.instance.author = author
        return super().save(*args, **kwargs)

        # if not self.instance.pk and commit:
        #     raise ValueError('PostForm commit=True save() is not allowed')
        # return super().save(*args, **kwargs)


class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
