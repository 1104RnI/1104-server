# Django
from django_filters.rest_framework import DjangoFilterBackend

# Bases
from cheonbaeksa.bases.api.viewsets import GenericViewSet

# Mixins
from cheonbaeksa.apps.orders.api.views.mixins import OrderPaymentViewMixin

# Permissions
from cheonbaeksa.apps.orders.api.views.permissions import OrderPermission

# Models
from cheonbaeksa.apps.orders.models import Order


# Main Section
class OrdersViewSet(OrderPaymentViewMixin,
                    GenericViewSet):
    queryset = Order.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (OrderPermission,)
