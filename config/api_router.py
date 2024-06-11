# Django
from django.urls import path

# DRF
from rest_framework_nested import routers

# User
from cheonbaeksa.apps.users.api.views.index import UsersViewSet

# Token
from cheonbaeksa.apps.users.api.views import CustomTokenRefreshView

# EmailVerification
from cheonbaeksa.apps.verifications.api.views import EmailVerificationsViewSet

# Router
router = routers.SimpleRouter(trailing_slash=False)

# User
router.register(r'users', UsersViewSet)
router.register(r'email-verifications', EmailVerificationsViewSet)

app_name = 'api'
urlpatterns = [
                  path('token/refresh', CustomTokenRefreshView.as_view(), name='custom_token_refresh'),
              ] + router.urls
