# Django
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from cheonbaeksa.bases.api import mixins
from cheonbaeksa.bases.api.viewsets import GenericViewSet

# Utils
from cheonbaeksa.utils.decorators import swagger_decorator

# Permissions
from cheonbaeksa.apps.verifications.api.views.permissions import EmailVerificationPermission

# Mixins
from cheonbaeksa.apps.verifications.api.views.mixins import EmailVerificationSignupViewMixin

# Serializers
from cheonbaeksa.apps.verifications.api.serializers import EmailVerificationListSerializer

# Models
from cheonbaeksa.apps.verifications.models import EmailVerification


# Main Section
class EmailVerificationsViewSet(EmailVerificationSignupViewMixin,
                                mixins.ListModelMixin,
                                GenericViewSet):
    serializers = {
        'default': EmailVerificationListSerializer,
    }
    queryset = EmailVerification.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (EmailVerificationPermission,)

    @swagger_auto_schema(**swagger_decorator(tag='이메일 인증',
                                             id='이메일 인증 리스트 조회',
                                             description='',
                                             response={200: EmailVerificationListSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
