# Django
from django.contrib import admin

# Bases
from cheonbaeksa.bases.admin import Admin, get_changed_fields

# Models
from cheonbaeksa.apps.histories.models import UserHistory
from cheonbaeksa.apps.coupons.models import Coupon, CouponGroup


# Main Section
@admin.register(CouponGroup)
class CouponGroupAdmin(Admin):
    list_display = ('user_id', 'title', 'discount_price', 'discount_percentage', 'valid_days', 'is_active')
    search_fields = ('user_id', 'title')
    list_filter = ('user_id',)

    fieldsets = (
        ('1. 정보', {'fields': ('user_id', 'title', 'discount_price', 'discount_percentage', 'valid_days', 'is_active')}),
        ('2. 날짜', {'fields': ('created', 'modified')}),
    )

    readonly_fields = ('created', 'modified', 'user_id')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user_id = request.user.id
            action = "Create"
            changed_fields = None
        else:
            old_obj = CouponGroup.objects.get(pk=obj.pk)
            action = "Update"
            changed_fields = get_changed_fields(old_obj, obj)

        obj.full_clean()
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


@admin.register(Coupon)
class CouponAdmin(Admin):
    list_display = ('user_id', 'coupon_group_id', 'code', 'discount_price', 'discount_percentage', 'is_used', 'expired')
    search_fields = ('user_id', 'coupon_group_id')
    list_filter = ('user_id', 'coupon_group_id', 'is_used')

    fieldsets = (
        ('1. 정보', {'fields': ('user_id', 'coupon_group_id', 'code', 'discount_price', 'discount_percentage',
                              'is_used')}),
        ('2. 날짜', {'fields': ('created', 'modified', 'expired')}),
    )

    readonly_fields = ('created', 'modified', 'user_id', 'is_used', 'expired', 'code')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user_id = request.user.id
            action = "Create"
            changed_fields = None
        else:
            old_obj = CouponGroup.objects.get(pk=obj.pk)
            action = "Update"
            changed_fields = get_changed_fields(old_obj, obj)

        obj.full_clean()
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
