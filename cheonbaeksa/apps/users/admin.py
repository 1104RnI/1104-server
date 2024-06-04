# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Bases
from cheonbaeksa.bases.admin import Admin

# Models
from cheonbaeksa.apps.users.models.index import User


# Define the UserChangeForm with custom validation
class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        trading_view_username = cleaned_data.get('trading_view_username')
        exchange_title = cleaned_data.get('exchange_title')
        exchange_uid = cleaned_data.get('exchange_uid')

        if trading_view_username and User.objects.filter(trading_view_username=trading_view_username).exclude(
            id=self.instance.id).exists():
            self.add_error('trading_view_username', ValidationError(_('이미 사용중인 트레이딩뷰 닉네임입니다.')))

        if exchange_uid and User.objects.filter(exchange_title=exchange_title, exchange_uid=exchange_uid).exclude(
            id=self.instance.id).exists():
            self.add_error('exchange_uid', ValidationError(_('이미 사용중인 거래소 UID입니다.')))

        return cleaned_data


@admin.register(User)
class UserAdmin(Admin, UserAdmin):
    form = UserChangeForm
    list_display = ('email', 'is_email_verified', 'trading_view_username', 'exchange_title', 'exchange_uid', 'is_staff')
    search_fields = ('email', 'trading_view_username', 'exchange_title', 'exchange_uid')
    list_filter = ('is_staff', 'is_email_verified', 'exchange_title')
    ordering = ('-created',)

    fieldsets = (
        ('1. 정보', {'fields': ('id', 'email', 'is_email_verified', 'auth_token')}),
        ('2. 추가 정보', {'fields': ('trading_view_username', 'exchange_title', 'exchange_uid')}),
        ('3. 권한', {'fields': ('is_staff',)}),
        ('4. 생성일 / 수정일', {'fields': ('created', 'modified')}),
    )

    add_fieldsets = (
        ('1. 정보', {'fields': ('email', 'name', 'password1', 'password2')}),
        ('2. 권한', {'fields': ('is_staff',)}),
    )

    readonly_fields = ('auth_token', 'created', 'modified', 'is_email_verified')
