import json
from collections import OrderedDict

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.inspectors import PaginatorInspector
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
from rest_framework.pagination import PageNumberPagination

from velait.velait_django.main.api.responses import APIResponse


class VelaitPagination(PageNumberPagination):
    def get_last_page(self):
        return replace_query_param(
            url=self.request.build_absolute_uri(),
            key=self.page_query_param,
            val=self.page.paginator.num_pages,
        )

    def __parse_page_param(self, request):
        try:
            parsed_page = json.loads(request.query_params['page'])

            if not isinstance(parsed_page, dict):
                raise TypeError()
            elif parsed_page.get('size') <= 0 or parsed_page.get('offset', 0) < 0:
                raise ValueError()

            return parsed_page

        except (json.JSONDecodeError, TypeError, ValueError, KeyError) as exc:
            return {'offset': 0, 'size': settings.REST_FRAMEWORK['PAGE_SIZE']}

    def get_page_size(self, request):
        page_param = self.__parse_page_param(request)
        if page_param:
            return page_param.get('size')

        return super(VelaitPagination, self).get_page_size(request)

    def get_page_number(self, request, paginator):
        page_param = self.__parse_page_param(request)

        if page_param:
            page = page_param.get('offset', 0) // page_param.get('size')
            if page <= 0:
                return 1
            return page

        return super(VelaitPagination, self).get_page_number(request, paginator)

    def get_paginated_response(self, data):
        return APIResponse({
            "pagination": {
                'totalRecords': self.page.paginator.count,
                'totalPages': self.page.paginator.num_pages,
                'first': self.request.build_absolute_uri(),
                'last': self.get_last_page(),
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            "results": data,
            "errors": [],
        })


class VelaitPaginationInspector(PaginatorInspector):
    def get_paginated_response(self, paginator, response_schema):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "pagination": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'totalRecords': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'totalPages': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'first': openapi.Schema(type=openapi.TYPE_STRING,
                                                format=openapi.FORMAT_URI, x_nullable=True),
                        'last': openapi.Schema(type=openapi.TYPE_STRING,
                                               format=openapi.FORMAT_URI, x_nullable=True),
                        'next': openapi.Schema(type=openapi.TYPE_STRING,
                                               format=openapi.FORMAT_URI, x_nullable=True),
                        'previous': openapi.Schema(type=openapi.TYPE_STRING,
                                                   format=openapi.FORMAT_URI, x_nullable=True),
                    },
                ),
                'results': response_schema,
                'errors': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
                ),
            },
            required=['results'],
        )
