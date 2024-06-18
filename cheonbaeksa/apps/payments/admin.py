# Django
from django.contrib import admin

# Bases
from cheonbaeksa.apps.payments.models import Payment
from cheonbaeksa.bases.admin import Admin

# Models
from cheonbaeksa.apps.products.models import Product


# Main Section
@admin.register(Payment)
class PaymentAdmin(Admin):
    list_display = ('user_id', 'order_id', 'imp_uid', 'total_price', 'status')
    search_fields = ('imp_uid',)
    list_filter = ('status',)

    fieldsets = (
        ('1. 정보', {'fields': ('user_id', 'order_id', 'imp_uid', 'total_price')}),
        ('2. 상태', {'fields': ('status', 'prepared_at', 'failed_at', 'paid_at', 'partial_cancelled_at',
                              'cancelled_at')}),
        ('3. 데이터', {'fields': ('pg_data',)}),
        ('4. 날짜', {'fields': ('created', 'modified')}),
    )

    readonly_fields = ('created', 'modified', 'prepared_at', 'failed_at', 'paid_at', 'partial_cancelled_at',
                       'cancelled_at', 'pg_data')
