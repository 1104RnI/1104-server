# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

# Inlines
from cheonbaeksa.apps.users.inlines import SocialAccountInline

# Bases
from cheonbaeksa.bases.admin import Admin

# Models
from cheonbaeksa.apps.users.models.index import User


@admin.register(User)
class UserAdmin(Admin, UserAdmin):
    list_display = ('email', 'name', 'is_staff')
    search_fields = ('email', 'name')
    list_filter = ('is_staff',)
    ordering = ('-created',)

    fieldsets = (
        ('1. 정보', {'fields': ('id', 'email', 'name', 'password', 'auth_token')}),
        ('2. 권한', {'fields': ('is_staff',)}),
        ('3. 생성일 / 수정일', {'fields': ('created', 'modified')}),
    )

    add_fieldsets = (
        ('1. 정보', {'fields': ('email', 'name', 'password1', 'password2')}),
        ('2. 권한', {'fields': ('is_staff',)}),
    )

    readonly_fields = ('auth_token', "created", "modified")
    inlines = (SocialAccountInline,)
