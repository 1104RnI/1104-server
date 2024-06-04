# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UsernameField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Bases
from cheonbaeksa.bases.admin import Admin

# Models
from cheonbaeksa.apps.users.models.index import User


# Define the UserChangeForm with custom validation
class UserCustomChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            'Raw passwords are not stored, so there is no way to see this '
            'user’s password, but you can change the password using '
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

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
    form = UserCustomChangeForm
    list_display = ('email', 'is_email_verified', 'trading_view_username', 'exchange_title', 'exchange_uid', 'is_staff')
    search_fields = ('email', 'trading_view_username', 'exchange_title', 'exchange_uid')
    list_filter = ('is_staff', 'is_email_verified', 'exchange_title')
    ordering = ('-created',)

    fieldsets = (
        ('1. 정보', {'fields': ('id', 'email', 'password', 'is_email_verified', 'auth_token')}),
        ('2. 추가 정보', {'fields': ('trading_view_username', 'exchange_title', 'exchange_uid')}),
        ('3. 권한', {'fields': ('is_staff',)}),
        ('4. 생성일 / 수정일', {'fields': ('created', 'modified')}),
    )

    add_fieldsets = (
        ('1. 정보', {'fields': ('email', 'name', 'password1', 'password2')}),
        ('2. 권한', {'fields': ('is_staff',)}),
    )

    readonly_fields = ('auth_token', 'created', 'modified', 'is_email_verified')
