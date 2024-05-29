from allauth.socialaccount.models import SocialAccount
from cheonbaeksa.bases.inlines import TabularInline


class SocialAccountInline(TabularInline):
    model = SocialAccount
    fk_name = 'user'
    fields = ('provider', 'uid')
    readonly_fields_update = ('provider', 'uid')
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return True
