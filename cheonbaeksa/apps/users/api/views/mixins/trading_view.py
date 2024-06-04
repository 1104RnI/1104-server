# Django
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework import status
from rest_framework.decorators import action

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator

# Serializers
from cheonbaeksa.apps.users.api.serializers import UserLoginSuccessSerializer, UserTradingViewUsernameUpdateSerializer


# Main Section
class UserTradingViewViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='트레이딩뷰 닉네임 수정',
                                             description='',
                                             request=UserTradingViewUsernameUpdateSerializer,
                                             response={200: UserLoginSuccessSerializer},
                                             ))
    @action(detail=False, methods=['patch'], url_path='trading-view-username')
    def update_trading_view_username(self, request):
        user = request.user
        serializer = UserTradingViewUsernameUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                status=status.HTTP_200_OK,
                code=200,
                message=_('ok'),
                data=UserLoginSuccessSerializer(instance=request.user).data
            )
