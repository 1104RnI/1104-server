# Django
from django.contrib import admin

# Bases
from cheonbaeksa.bases.admin import Admin

# Models
from cheonbaeksa.apps.products.models import Product


# Main Section
@admin.register(Product)
class ProductAdmin(Admin):
    list_display = ('title', 'price', 'subscription_price', 'description')
    search_fields = ('title',)
    list_filter = ()

    fieldsets = (
        ('1. 정보', {'fields': ('title', 'price', 'subscription_price', 'description')}),
        ('2. 날짜', {'fields': ('created', 'modified')}),
    )

    readonly_fields = ('created', 'modified')
