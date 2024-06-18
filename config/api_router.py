# Django
from django.urls import path

# DRF
from rest_framework_nested import routers

# User
from cheonbaeksa.apps.users.api.views import UsersViewSet

# Coupon
from cheonbaeksa.apps.coupons.api.views import CouponsViewSet

# Product
from cheonbaeksa.apps.products.api.views.index import ProductsViewSet

# Token
from cheonbaeksa.apps.users.api.views import CustomTokenRefreshView

# EmailVerification
from cheonbaeksa.apps.verifications.api.views import EmailVerificationsViewSet

# Order
from cheonbaeksa.apps.orders.api.views import OrdersViewSet

# Router
router = routers.SimpleRouter(trailing_slash=False)

# User
router.register('users', UsersViewSet)

# Verification
router.register(r'email-verifications', EmailVerificationsViewSet)

# Coupon
router.register('coupons', CouponsViewSet)

# Product
router.register('products', ProductsViewSet)

# Product
router.register('orders', OrdersViewSet)

app_name = 'api'
urlpatterns = [
                  path('token/refresh', CustomTokenRefreshView.as_view(), name='custom_token_refresh'),
              ] + router.urls
