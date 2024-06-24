# Django
from django.contrib import admin

# Bases
from cheonbaeksa.bases.admin import Admin

# Models
from cheonbaeksa.apps.histories.models import UserHistory


# Main Section
@admin.register(UserHistory)
class UserHistoryAdmin(Admin):
    list_display = ('user_id', 'description')
    search_fields = ('user_id', 'description')
    list_filter = ()

    fieldsets = (
        ('1. 정보', {'fields': ('user_id', 'description', 'action', 'model_title', 'object_id', 'changed_fields')}),
        ('2. 날짜', {'fields': ('created', 'modified')}),
    )

    readonly_fields = ('created', 'modified', 'user_id', 'description', 'action', 'model_title', 'object_id',
                       'changed_fields')
