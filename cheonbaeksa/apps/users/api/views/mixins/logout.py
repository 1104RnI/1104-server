# Django
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import logout

# DRF
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

# Third Party
from drf_yasg.utils import swagger_auto_schema, no_body

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator


# Main Section
class UserLogoutViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='로그아웃',
                                             description="""
                                             사용자를 로그아웃 처리합니다. 요청 시 헤더에 유효한 토큰을 포함해야 합니다.
                                             """,
                                             request=no_body,
                                             response={200: 'ok'}
                                             ))
    @action(detail=False, methods=['post'], url_path='logout')
    def user_logout(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # 클라이언트의 refresh token을 무효화
            refresh_token = request.COOKIES.get('refresh_token')
            print('refresh_token : ', refresh_token)
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except Exception as e:
                    raise ValidationError(_('토큰 무효화 중 오류가 발생했습니다: ') + str(e))

            # 로그아웃 처리
            logout(request)

            # 클라이언트의 쿠키에서 refresh token 삭제
            response = Response(
                status=status.HTTP_200_OK,
                code=200,
                message=_('로그아웃이 완료되었습니다.'),
            )
            response.delete_cookie('refresh_token')
            return response
