from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from ..forms import PostForm, CommentForm
from ..models import Post

__all__ = (
    'post_list',
    'post_detail',
    'post_create',
    'post_delete',
    'post_like_toggle',
)


def post_list(request):
    """
    모든 Post목록을 리턴
    template은 'post/post_list.html'을 사용
    :param request:
    :return:
    """
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    # 해당 post의 사진을 img태그로 출력
    # 1. view작성
    #   1-1. post_pk에 해당하는 Post객체를
    #           post변수에 할당해서
    #           post라는 키로 context에 할당해서 render에 전달
    #   1-2. 템플릿은 post/post_detail.html사용

    # 2. url작성
    #   2-1. urls.py에 '/post/<post_pk>/에 해당하는 url에 이 view를 연결

    # 3. 템플릿 작성
    #   3-1. post/post_detail.html을 생성, 전달받은 'post'변수의
    #       photo필드의 url속성을 이용해 img태그 출력

    # 4. base템플릿 작성 및 'extend'템플릿태그 사용
    #   html:5 emmet을 사용, 기본이 되는 base.html을 작성, 나머지 템플릿에서 해당 템플릿을 extend
    #   내용은 'content' block에 채운다
    # post = Post.objects.get(pk=post_pk)
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)


@login_required
def post_create(request):
    """
    1. 이 뷰에 접근할 때, 해당 사용자가 인증된 상태가 아니면 로그인 뷰로 redirect
        is_authenticated

    2. form.is_valid()를 통과한 후, 생성하는 Post객체에 author정보를 추가
        request.user

    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        return redirect('member:login')

    if request.method == 'POST':
        # POST요청의 경우 PostForm인스턴스 생성과정에서 request.POST, request.FILES를 사용
        form = PostForm(request.POST, request.FILES)
        # form생성과정에서 전달된 데이터들이 Form의 모든 field들에 유효한지 검사
        if form.is_valid():
            # 유효할 경우 Post인스턴스를 생성 및 저장

            # 1. 커스텀 메서드 사용
            # form.save(author=request.user)

            # 2. 기존 Django의 ModelForm방식 사용
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:post_list')
    else:
        # GET요청의 경우, 빈 PostForm인스턴스를 생성해서 템플릿에 전달
        form = PostForm()

    # GET요청에선 이부분이 무조건 실행
    # POST요청에선 form.is_valid()를 통과하지 못하면 이부분이 실행
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_delete(request, post_pk):
    if not request.user.is_authenticated:
        return redirect('member:login')

    if request.method == 'POST':
        # post_pk에 해당하는 Post가 있는지 검사
        post = get_object_or_404(Post, pk=post_pk)
        # request.user가 Post의 author인지 검사
        if post.author == request.user:
            post.delete()
            return redirect('post:post_list')
        else:
            raise PermissionDenied('작성자가 아닙니다')


@login_required
def post_like_toggle(request, post_pk):
    """
    1. view, url연결
        /post/<post_pk>/like-toggle/

    2. 로직구현
        post_pk에 해당하는 Post가
        현재 로그인한 유저의 like_posts에 있다면 없애고
        like_posts에 없다면 추가

    3. post.html에서 현재 user가 해당 post를 like했는지 여부 표시
        {% if <A> in <B> %}

    4. post.html에서 이 뷰로 요청을 보낼 수 있는 form구현

    :param request:
    :param post_pk:
    :return:
    """
    if request.method == 'POST':
        # GET파라미터로 전달된 이동할 URL
        next_path = request.GET.get('next')

        # post_pk에 해당하는 Post객체
        post = get_object_or_404(Post, pk=post_pk)

        # 요청한 사용자
        user = request.user

        # 사용자의 like_posts목록에서 like_toggle할 Post가 있는지 확인
        filtered_like_posts = user.like_posts.filter(pk=post.pk)
        # 존재할경우, like_posts목록에서 해당 Post를 삭제
        if filtered_like_posts.exists():
            user.like_posts.remove(post)
        # 없을 경우, like_posts목록에 해당 Post를 추가
        else:
            user.like_posts.add(post)

        # 이동할 path가 존재할 경우 해당 위치로, 없을 경우 Post상세페이지로 이동
        if next_path:
            return redirect(next_path)
        return redirect('post:post_detail', post_pk=post_pk)
