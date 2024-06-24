# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UsernameField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Bases
from cheonbaeksa.bases.admin import Admin, get_changed_fields

# Models
from cheonbaeksa.apps.histories.models import UserHistory
from cheonbaeksa.apps.users.models import User


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
    list_display = ('email', 'is_email_verified', 'advisor_id', 'is_staff')
    search_fields = ('email', 'advisor_id')
    list_filter = ('is_staff', 'advisor_id', 'is_email_verified')
    ordering = ('-created',)

    fieldsets = (
        ('1. 정보', {'fields': ('id', 'email', 'password', 'is_email_verified',)}),
        ('2. 어드바이저', {'fields': ('advisor_id',)}),
        ('3. 권한', {'fields': ('is_staff',)}),
        ('4. 생성일 / 수정일', {'fields': ('created', 'modified')}),
    )

    add_fieldsets = (
        ('1. 정보', {'fields': ('email', 'password1', 'password2')}),
        ('2. 권한', {'fields': ('is_staff',)}),
    )

    readonly_fields = ('created', 'modified')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            action = "Create"
            changed_fields = None
        else:
            old_obj = User.objects.get(pk=obj.pk)
            action = "Update"
            changed_fields = get_changed_fields(old_obj, obj)

        super().save_model(request, obj, form, change)

        # UserHistory
        model_title = obj._meta.verbose_name
        description = f"User ID: {request.user.id}, Action: {action}, {model_title} ID: {obj.id}"
        if changed_fields:
            description += f", Changed Fields: {', '.join(changed_fields)}"
        UserHistory.objects.create(
            user_id=request.user.id,
            action=action,
            model_title=model_title,
            object_id=obj.id,
            description=description,
            changed_fields="\n".join(changed_fields) if changed_fields else ""
        )

    def delete_model(self, request, obj):
        # UserHistory
        model_title = obj._meta.verbose_name
        description = f"User ID: {request.user.id}, Action: Delete, {model_title} ID: {obj.id}"
        UserHistory.objects.create(
            user_id=request.user.id,
            action="Delete",
            model_title=model_title,
            object_id=obj.id,
            description=description
        )
        super().delete_model(request, obj)
