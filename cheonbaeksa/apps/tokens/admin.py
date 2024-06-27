# Django
from django.contrib import admin

# Bases
from cheonbaeksa.bases.admin import Admin

# Models
from cheonbaeksa.apps.tokens.models import PasswordResetToken


# Main Section
@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(Admin):
    list_display = ('user_id', 'token', 'expired')
    search_fields = ('user_id', 'token',)
    list_filter = ('user_id',)

    fieldsets = (
        ('1. 정보', {'fields': ('user_id', 'token', 'expired')}),
        ('2. 날짜', {'fields': ('created', 'modified')}),
    )

    readonly_fields = ('created', 'modified', 'user_id', 'token', 'expired')
