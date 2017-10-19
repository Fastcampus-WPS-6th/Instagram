"""
post_list뷰를 'post/' URL에 할당
"""
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm, CommentForm
from .models import Post, PostComment


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


def post_create(request):
    """
    Post를 생성
    반드시 photo필드에 해당하는 파일이 와야한다
    :param request:
    :return:

    1. post_create.html파일을 만들고
         /post/create/ URL로 요청이 온 경우
         이 뷰에서 해당 파일을 render해서 response

    2. post_create.html에 form을 만들고,
        file input과 button요소를 배치
        file input의 name은 'photo'로 지정

    3. 이 뷰에서 request.method가 'POST'일 경우,
        request.POST와 request.FILES를 print문으로 출력
        'GET'이면 템플릿파일을 보여주는 기존 로직을 그대로 실행
    """
    if request.method == 'POST':
        # POST요청의 경우 PostForm인스턴스 생성과정에서 request.POST, request.FILES를 사용
        form = PostForm(request.POST, request.FILES)
        # form생성과정에서 전달된 데이터들이 Form의 모든 field들에 유효한지 검사
        if form.is_valid():
            # 유효할 경우 Post인스턴스를 생성 및 저장
            Post.objects.create(
                photo=form.cleaned_data['photo'])
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


def comment_create(request, post_pk):
    """
    post_pk에 해당하는 Post에 연결된 PostComment를 작성
    PostComment Form을 생성해서 사용
    기본적인 루틴은 위의 post_create와 같음
    :param request:
    :param post_pk:
    :return:
    """
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
            PostComment.objects.create(
                post=post,
                content=form.cleaned_data['content']
            )
            # 생성 후 Post의 detail화면으로 이동
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('post:post_detail', post_pk=post_pk)