# Django
from django.contrib import admin

# Bases
from cheonbaeksa.bases.admin import Admin, get_changed_fields

# Models
from cheonbaeksa.apps.histories.models import UserHistory
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

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user_id = request.user.id
            action = "Create"
            changed_fields = None
        else:
            old_obj = Product.objects.get(pk=obj.pk)
            action = "Update"
            changed_fields = get_changed_fields(old_obj, obj)

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
