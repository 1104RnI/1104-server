# Django
from django.contrib import admin

# Bases
from cheonbaeksa.bases.admin import Admin

# Models
from cheonbaeksa.apps.orders.models import Order


# Main Section
@admin.register(Order)
class OrderAdmin(Admin):
    list_display = ('user_id', 'product_id', 'coupon_id', 'number', 'total_price', 'status')
    search_fields = ('user_id', 'product_id', 'coupon_id', 'number')
    list_filter = ('user_id', 'product_id', 'status')

    fieldsets = (
        ('1. 정보', {'fields': ('user_id', 'product_id', 'coupon_id', 'number', 'total_price')}),
        ('2. 상태', {'fields': ('status', 'pending_at', 'approved_at', 'refused_at')}),
        ('3. 활성화', {'fields': ('is_active',)}),
        ('4. 날짜', {'fields': ('created', 'modified')}),
    )

    readonly_fields = ('created', 'modified', 'user_id', 'product_id', 'coupon_id', 'number', 'total_price', 'status',
                       'pending_at', 'approved_at', 'refused_at')
