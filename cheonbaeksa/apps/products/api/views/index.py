# Django
from django_filters.rest_framework import DjangoFilterBackend

# Bases
from cheonbaeksa.bases.api.viewsets import GenericViewSet

# Mixins
from cheonbaeksa.apps.products.api.views.mixins import ProductOrderViewMixin

# Permissions
from cheonbaeksa.apps.products.api.views.permissions import ProductPermission

# Models
from cheonbaeksa.apps.products.models import Product


# Main Section
class ProductsViewSet(ProductOrderViewMixin,
                      GenericViewSet):
    queryset = Product.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (ProductPermission,)
