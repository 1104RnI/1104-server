# Django
from django.conf import settings
from django.urls import include, path
from django.utils.translation import ugettext_lazy as _

# DRF
from rest_framework import permissions

# Third party
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

description = _(
    """
1104 백엔드 서버 API 문서입니다.

# Response Data
<br/>
## 성공
```json
{
    "code": 200,
    "message": "ok",
    "count": 1,
    "next": null,
    "previous": null,
    "data": [
        {
            "id": 8,
            "email": "user3@example.com",
            "is_email_verified": false
        },
        ...
    ]
}
```
<br/>
## 실패
```json
{
    "code": 403,
    "message": "접근 권한이 없습니다.",
    "errors": {
        "field_errors": {},
        "non_field_errors": [
            "Invalid email or password."
        ]
    }
}
```

<br/>
## 세부 안내

- `code`: HTTP 상태 코드입니다.
- `message`: 응답에 대한 설명 메시지입니다. 성공 시 "ok", 실패 시 오류 메시지를 포함합니다.
- `count`: GET 요청 시 반환되는 데이터의 총 개수입니다. 주로 리스트 조회 시 사용됩니다.
- `next`: 페이징 처리 시 다음 페이지의 URL입니다. 더 이상의 페이지가 없을 경우 null입니다.
- `previous`: 페이징 처리 시 이전 페이지의 URL입니다. 첫 페이지인 경우 null입니다.
- `data`: 응답의 주요 데이터를 포함하는 필드입니다. 성공 시 반환되는 데이터가 이 필드에 포함됩니다.
- `errors`: 오류 발생 시 나타나는 필드입니다. `field_errors`와 `non_field_errors`를 포함합니다.
  - `field_errors`: 특정 필드와 관련된 오류 메시지입니다. 각 필드의 오류 메시지를 키-값 쌍으로 포함합니다.
  - `non_field_errors`: 특정 필드와 관련되지 않은 일반 오류 메시지입니다. 예를 들어, 인증 실패와 같은 경우에 사용됩니다.

<br/>"""
)

# Only expose to public in local and development.
public = bool(settings.DJANGO_ENV in ('local',))

# Fully exposed to only for local, else at least should be staff.
if settings.DJANGO_ENV == "local":
    permission_classes = (permissions.AllowAny,)
else:
    # permission_classes = (permissions.IsAdminUser,)
    permission_classes = (permissions.AllowAny,)

schema_url_patterns = [
    path(r"^api/", include("config.api_router")),
]

schema_view = get_schema_view(
    openapi.Info(
        title=_("1104 API Document"),
        default_version="v1",
        description=description,
        # contact=openapi.Contact(email=""),
        # license=openapi.License(name=""),
    ),
    public=public,
    permission_classes=permission_classes,
    patterns=schema_url_patterns,
)
