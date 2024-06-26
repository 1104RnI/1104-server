# Django
from django_filters.rest_framework import DjangoFilterBackend

# Bases
from cheonbaeksa.bases.api.viewsets import GenericViewSet

# Mixins
from cheonbaeksa.apps.payments.api.views.mixins import PaymentConfirmViewMixin, PaymentNotifyViewMixin

# Permissions
from cheonbaeksa.apps.payments.api.views.permissions import PaymentPermission

# Models
from cheonbaeksa.apps.payments.models import Payment


# Main Section
class PaymentsViewSet(PaymentConfirmViewMixin,
                      PaymentNotifyViewMixin,
                      GenericViewSet):
    queryset = Payment.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (PaymentPermission,)
