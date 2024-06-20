# Django
from django_filters.rest_framework import DjangoFilterBackend

# Bases
from cheonbaeksa.bases.api.viewsets import GenericViewSet

# Mixins
from cheonbaeksa.apps.users.api.views.mixins import UserSignupViewMixin, UserLoginViewMixin, UserMeViewMixin, \
    UserPasswordViewMixin, UserPaymentViewMixin

# Permissions
from cheonbaeksa.apps.users.api.views.permissions import UserPermission

# Models
from cheonbaeksa.apps.users.models import User


# Main Section
class UsersViewSet(UserSignupViewMixin,
                   UserLoginViewMixin,
                   UserMeViewMixin,
                   UserPasswordViewMixin,
                   UserPaymentViewMixin,
                   GenericViewSet):
    queryset = User.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (UserPermission,)
