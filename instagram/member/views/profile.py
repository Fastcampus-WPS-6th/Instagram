from django.contrib.auth import get_user_model
from django.http import HttpResponse

from member.decorators import login_required

User = get_user_model()

__all__ = (
    'profile',
)


@login_required
def profile(request):
    return HttpResponse(f'User profile page {request.user}')
