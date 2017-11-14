from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect

from ..forms import CommentForm
from ..models import Post, PostComment

__all__ = (
    'comment_create',
    'comment_delete',
)


def comment_create(request, post_pk):
    """
    로그인한 유저만 요청 가능하도록 함
    작성하는 Comment에 author정보 추가

    :param request:
    :param post_pk:
    :return:
    """
    if not request.user.is_authenticated:
        return redirect('member:login')

    # URL get parameter로 온 'post_pk'에 해당하는
    # Post instance를 'post'변수에 할당
    # 찾지못하면 404Error를 브라우저에 리턴
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        # 데이터가 바인딩된 CommentForm인스턴스를 form에 할당
        form = CommentForm(request.POST)
        # 유효성 검증
        if form.is_valid():
            # 통과한 경우, post에 해당하는 Comment인스턴스를 생성
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            # GET parameter로 'next'값이 전달되면
            # 공백을 없애고 다음에 redirect될 주소로 지정
            next = request.GET.get('next', '').strip()
            # 다음에 갈 URL (next)가 빈 문자열이 아닌 경우
            if next:
                # 해당 next url로 이동
                return redirect(next)
            # 지정되지 않으면 post_detail로 이동
            return redirect('post:post_detail', post_pk=post_pk)


def comment_delete(request, comment_pk):
    next_path = request.GET.get('next', '').strip()

    if request.method == 'POST':
        comment = get_object_or_404(PostComment, pk=comment_pk)
        if comment.author == request.user:
            comment.delete()
            if next_path:
                return redirect(next_path)
            return redirect('post:post_detail', post_pk=comment.post.pk)
        else:
            raise PermissionDenied('작성자가 아닙니다')
