# DRF
from rest_framework_nested import routers

# User
from cheonbaeksa.apps.users.api.views.index import UsersViewSet

# Router
router = routers.SimpleRouter(trailing_slash=False)

# User
router.register(r'users', UsersViewSet)

app_name = 'api'
urlpatterns = [
              ] + router.urls
