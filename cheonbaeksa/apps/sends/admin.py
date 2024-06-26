# Django
from django.contrib import admin

# Bases
from cheonbaeksa.bases.admin import Admin

# Models
from cheonbaeksa.apps.sends.models import EmailSend


# Main Section
@admin.register(EmailSend)
class EmailSendAdmin(Admin):
    list_display = ('sender_email', 'recipient_email', 'title', 'purpose', 'status')
    search_fields = ('sender_email', 'recipient_email', 'title')
    list_filter = ('purpose', 'status')

    fieldsets = (
        ('1. 정보', {'fields': ('sender_email', 'recipient_email', 'title', 'content', 'purpose')}),
        ('2. 상태', {'fields': ('status',)}),
        ('3. 활성화', {'fields': ('is_active',)}),
        ('4. 날짜', {'fields': ('created', 'modified')}),
    )

    readonly_fields = ('created', 'modified', 'status')
