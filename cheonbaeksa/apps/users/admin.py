# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Bases
from cheonbaeksa.bases.admin import Admin

# Models
from cheonbaeksa.apps.users.models.index import User


@admin.register(User)
class UserAdmin(Admin, UserAdmin):
    list_display = ('email', 'is_email_verified', 'is_staff')
    search_fields = ('email', 'name')
    list_filter = ('is_staff', 'is_email_verified')
    ordering = ('-created',)

    fieldsets = (
        ('1. 정보', {'fields': ('id', 'email', 'is_email_verified', 'password', 'auth_token')}),
        ('2. 권한', {'fields': ('is_staff',)}),
        ('3. 생성일 / 수정일', {'fields': ('created', 'modified')}),
    )

    add_fieldsets = (
        ('1. 정보', {'fields': ('email', 'name', 'password1', 'password2')}),
        ('2. 권한', {'fields': ('is_staff',)}),
    )

    readonly_fields = ('auth_token', 'created', 'modified', 'is_email_verified')
