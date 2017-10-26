from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import SignupForm
from .models import User, Relation


class RelationInline(admin.TabularInline):
    model = Relation
    fk_name = 'from_user'
    extra = 1


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {'fields': (
            'img_profile',
            'age',
            'user_type',
            'like_posts',
        )}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {
            'fields': (
                'img_profile',
                'age',
                'user_type',
            ),
        }),
    )
    add_form = SignupForm
    inlines = [RelationInline,]

admin.site.register(User, UserAdmin)
