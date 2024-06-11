# DRF
from rest_framework import status
from rest_framework.views import APIView

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from django.utils.translation import gettext_lazy as _
from cheonbaeksa.utils.api.response import Response

# Serializers
from cheonbaeksa.apps.users.api.serializers import CustomTokenRefreshSerializer


# Main Section
class CustomTokenRefreshView(APIView):
    @swagger_auto_schema(
        tags=['토큰'],
        operation_id='토큰 재발급',
        operation_description='Refresh Token을 사용하여 Access Token을 재발급 받습니다.',
        request_body=CustomTokenRefreshSerializer,
        responses={200: 'ok', 400: 'Invalid Token'}
    )
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                status=status.HTTP_200_OK,
                code=200,
                message=_('토큰이 재발급되었습니다.'),
                data=serializer.validated_data
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                code=400,
                message=_('유효하지 않은 토큰입니다.'),
                errors=serializer.errors
            )
