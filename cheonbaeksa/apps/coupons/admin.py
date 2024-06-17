# Django
from django.contrib import admin

# Bases
from rest_framework.exceptions import ValidationError

from cheonbaeksa.bases.admin import Admin

# Models
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
        obj.full_clean()
        super().save_model(request, obj, form, change)


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
        obj.full_clean()
        super().save_model(request, obj, form, change)
