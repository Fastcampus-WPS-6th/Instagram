from django import forms

from .models import Post, PostComment

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

        # 새로 저장하려는 객체이며(pk값이 없음), DB에 바로 저장하려고 할 경우(commit=True)
        if not self.instance.pk and commit:
            # author값을 키워드인수 묶음에서 pop으로 삭제하며 값을 가져온다
            author = kwargs.pop('author', None)
            # author값이 없을경우 (키워드가 없었거나 값이 주어지지 않거나)
            if not author:
                # ValueError를 발생시킴
                raise ValueError('Author field is required')
            # author값이 존재하면 자신의 instance의 author필드값을 채움
            self.instance.author = author
        # 슈퍼클래스의 save를 호출
        return super().save(*args, **kwargs)

        # if not self.instance.pk and commit:
        #     raise ValueError('PostForm commit=True save() is not allowed')
        # return super().save(*args, **kwargs)


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = (
            'content',
        )
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }
