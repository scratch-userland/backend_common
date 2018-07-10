# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from sqlalchemy import asc
from sqlalchemy import desc
from werkzeug.exceptions import HTTPException

from .exception import \
    ApiException, NotFoundException, BadRequestException, \
    UnauthorizedException, ForbiddenException


class RestfulBase(Resource):
    _model_service = None

    def pre_request(f):
        def method(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ApiException, ex:
                return ex.__str__(), ex.http_status_code
            except HTTPException, ex:
                return ex.get_response()
        return method
    method_decorators = [pre_request]

    def get_context_data(self, *fields, **arguments):
        return {k: v for k, v in arguments.items() if k in fields}

    def filter_valid_args(self, **args):
        for k, v in args.items():
            if v is not None:
                continue
            args.pop(k)


def parse_page(sorted_fields={}, default_sort_field=None, sort_order='desc'):
    parser = reqparse.RequestParser()
    parser.add_argument('page', type=int, default=1, location=['args'])
    parser.add_argument('per_page', type=int, default=10, location=['args'])
    parser.add_argument('sort_order', type=str, choices=['asc', 'desc'], default='desc', location=['args'])
    parser.add_argument('sort_field', type=str, location=['args'])
    parser.add_argument('keyword', type=unicode, location=['args'])
    args = parser.parse_args()

    if sort_order == 'asc' and default_sort_field:
        sort_field = asc(default_sort_field)
    else:
        sort_field = desc(default_sort_field) if default_sort_field else None

    if args['sort_field'] in sorted_fields.keys():
        if args['sort_order'] == 'asc':
            sort_field = asc(args['sort_field'])
        elif args['sort_order'] == 'desc':
            sort_field = desc(args['sort_field'])

    return {
        'page': args['page'],
        'per_page': args['per_page'],
        'sort_field': sort_field,
        'keyword': args['keyword'],
    }


def raise_error_response(error_code, message='error', data=None):
    raise ApiException(error_code, message, data)


def raise_400_response(code=400, message=u'请求参数错误', data=None):
    raise BadRequestException(code=code, message=message, data=data)


def raise_401_response(code=401, message=u'请求未授权', data=None):
    raise UnauthorizedException(code=code, message=message, data=data)


def raise_403_response(code=403, message=u'请求被拒绝', data=None):
    raise ForbiddenException(code=code, message=message, data=data)


def raise_404_response(code=404, message=u'未找到', data=None):
    raise NotFoundException(code=code, message=message, data=data)


def success_response(message='success', data=None):
    result = {
        'code': 0,
        'message': message
    }
    if data is not None:
        result['data'] = data

    return result, 200
