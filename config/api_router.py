# Django
from django.urls import include, path

# DRF
from rest_framework_nested import routers

# Router
router = routers.SimpleRouter(trailing_slash=False)

app_name = 'api'
urlpatterns = [
              ] + router.urls
