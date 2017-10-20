from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import SignupForm
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('img_profile', 'age', 'like_posts')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {
            'fields': ('img_profile', 'age',),
        }),
    )
    add_form = SignupForm


admin.site.register(User, UserAdmin)
