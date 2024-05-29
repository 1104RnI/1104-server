# Python
import operator
from functools import reduce

# Django
from django.db import models
from django.utils.encoding import force_str
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework.filters import SearchFilter
from rest_framework.compat import coreapi, coreschema, distinct

# Models
from cheonbaeksa.apps.searches.models import SearchHistory


# Main Section
class AdvancedSearchFilter(SearchFilter):
    search_or_param = 'or'
    search_or_title = _('Search')
    search_or_description = _('A search term.')

    search_and_param = 'and'
    search_and_title = _('Search')
    search_and_description = _('A search term.')

    search_exclude_param = 'exclude'
    search_exclude_title = _('Search')
    search_exclude_description = _('A search term.')

    def get_search_terms(self, request, param=None):
        params = request.query_params.get(param, '')

        # 사용자가 인증되었고, 검색어가 비어있지 않은 경우 처리
        if request.user.is_authenticated and params:
            # update_or_create 메서드를 사용하여 동일 검색어 처리
            # 검색 기록이 이미 존재하면 created_at을 현재 시간으로 업데이트하고,
            # 존재하지 않으면 새로운 검색 기록을 생성합니다.
            SearchHistory.objects.update_or_create(
                user=request.user,
                content=params,
                defaults={'created': now()}
            )

        params = params.replace('\x00', '')
        params = params.replace(',', ' ')
        return params.split()

    def get_all_search_terms(self, request):
        all_search_terms = {'or': [], 'and': [], 'exclude': []}
        for search_param in [self.search_param, 'or', 'and', 'exclude']:
            search_terms = self.get_search_terms(request, search_param)
            if search_terms:
                if search_param == 'and':
                    all_search_terms['and'] = search_terms
                elif search_param == 'exclude':
                    all_search_terms['exclude'] = search_terms
                else:
                    all_search_terms['or'] += search_terms

        return all_search_terms

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        all_search_terms = self.get_all_search_terms(request)

        if not search_fields or not (
            len(all_search_terms['or']) or len(all_search_terms['and']) or len(all_search_terms['exclude'])):
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field))
            for search_field in search_fields
        ]

        base = queryset

        for param in ['or', 'and', 'exclude']:
            terms = all_search_terms[param]

            if not terms:
                continue

            def get_queries(_term):
                return [models.Q(**{orm_lookup: _term}) for orm_lookup in orm_lookups]

            conditions = []
            for term in terms:
                conditions.append(reduce(operator.or_, get_queries(term)))

            if conditions:
                if param == 'or':
                    queryset = queryset.filter(reduce(operator.or_, conditions))
                elif param == 'and':
                    queryset = queryset.filter(reduce(operator.and_, conditions))
                elif param == 'exclude':
                    queryset = queryset.exclude(reduce(operator.or_, conditions))

        if self.must_call_distinct(queryset, search_fields):
            queryset = distinct(queryset, base)

        return queryset

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=self.search_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str(self.search_title),
                    description=force_str(self.search_description)
                )
            ),
            coreapi.Field(
                name=self.search_or_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str(self.search_title),
                    description=force_str(self.search_description)
                )
            ),
            coreapi.Field(
                name=self.search_and_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str(self.search_title),
                    description=force_str(self.search_description)
                )
            ),
            coreapi.Field(
                name=self.search_exclude_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str(self.search_title),
                    description=force_str(self.search_description)
                )
            ),
        ]
