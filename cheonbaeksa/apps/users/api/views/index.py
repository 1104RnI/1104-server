# Django
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from cheonbaeksa.bases.api import mixins
from cheonbaeksa.bases.api.viewsets import GenericViewSet

# Utils
from cheonbaeksa.utils.decorators import swagger_decorator

# Mixins
from cheonbaeksa.apps.users.api.views.mixins import UserSignupViewMixin, UserLoginViewMixin

# Permissions
from cheonbaeksa.apps.users.api.views.permissions import UserPermission

# Serializers
from cheonbaeksa.apps.users.api.serializers import UserListSerializer

# Models
from cheonbaeksa.apps.users.models import User


# Main Section
class UsersViewSet(UserSignupViewMixin,
                   UserLoginViewMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializers = {
        'default': UserListSerializer,
    }
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (UserPermission,)

    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='유저 리스트 조회',
                                             description='',
                                             response={200: UserListSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
