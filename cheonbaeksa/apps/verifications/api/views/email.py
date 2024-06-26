# Django
from django_filters.rest_framework import DjangoFilterBackend

# Bases
from cheonbaeksa.bases.api.viewsets import GenericViewSet

# Permissions
from cheonbaeksa.apps.verifications.api.views.permissions import EmailVerificationPermission

# Mixins
from cheonbaeksa.apps.verifications.api.views.mixins import EmailVerificationSignupViewMixin, \
    EmailVerificationSignupVerifyViewMixin, EmailVerificationPasswordResetViewMixin, \
    EmailVerificationPasswordResetVerifyViewMixin

# Models
from cheonbaeksa.apps.verifications.models import EmailVerification


# Main Section
class EmailVerificationsViewSet(EmailVerificationSignupViewMixin,
                                EmailVerificationSignupVerifyViewMixin,
                                EmailVerificationPasswordResetViewMixin,
                                EmailVerificationPasswordResetVerifyViewMixin,
                                GenericViewSet):
    queryset = EmailVerification.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (EmailVerificationPermission,)
