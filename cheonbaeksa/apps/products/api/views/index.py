# Django
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from cheonbaeksa.bases.api import mixins
from cheonbaeksa.bases.api.viewsets import GenericViewSet

# Mixins
from cheonbaeksa.apps.products.api.views.mixins import ProductOrderViewMixin

# Permissions
from cheonbaeksa.apps.products.api.views.permissions import ProductPermission

# Serializers
from cheonbaeksa.apps.products.api.serializers import ProductListSerializer

# Models
from cheonbaeksa.apps.products.models import Product

# Main Section
from cheonbaeksa.utils.decorators import swagger_decorator


class ProductsViewSet(ProductOrderViewMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    serializers = {
        'default': ProductListSerializer,
    }

    queryset = Product.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (ProductPermission,)

    @swagger_auto_schema(**swagger_decorator(tag='상품',
                                             id='상품 리스트 조회',
                                             description='',
                                             response={200: ProductListSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
