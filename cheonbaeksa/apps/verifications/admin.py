# Django
from django.contrib import admin

# Bases
from cheonbaeksa.bases.admin import Admin

# Models
from cheonbaeksa.apps.verifications.models import EmailVerification


# Main Section
@admin.register(EmailVerification)
class EmailVerificationAdmin(Admin):
    list_display = ('user', 'email', 'code', 'purpose', 'is_verified', 'expired')
    search_fields = ('email',)
    list_filter = ('purpose', 'is_verified')

    fieldsets = (
        ('1. 정보', {'fields': ('user', 'email', 'code', 'purpose', 'is_verified',)}),
        ('2. 날짜', {'fields': ('created', 'modified', 'expired')}),
    )

    readonly_fields = ('created', 'modified', 'expired')
