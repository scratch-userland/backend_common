# -*- coding: utf-8 -*-

from flask import current_app, jsonify
from flask import g
from flask import request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from ..api import raise_401_response
from ...extensions import bcrypt


def _unauthorized():
    response = jsonify({'code': 401, 'message': u'请登录'})
    response.status_code = 401
    return response


class BaseSecurity(object):

    _model = None

    _auth_model = None

    _ignore_auth = False

    def _get_user_from_auth_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'], salt=current_app.config['SECRET_SALT'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return self._model.get_by_id(data['id'])

    def _verify_password(self, access_id_or_token, password):
        token = request.values.get('token', None)

        if request.method == 'OPTIONS' and not token:
            return True

        # 是否忽略验证
        if self._ignore_auth:
            return True

        # 登录名、密码登录
        if access_id_or_token and password:
            user_auth = self._auth_model.query.filter_by(access_id=access_id_or_token).first()
            if not user_auth or not user_auth.user:
                raise_401_response(message=u'该用户未注册')
            user = user_auth.user

            # FIXME: 0需要与数据库常量同步
            if (not user) or user.status != 0:
                raise_401_response(message=u'该用户未注册')
            if bcrypt.check_password_hash(user_auth.access_token, password):
                g.current_user = user
                g.token_used = False
                return True
            else:
                raise_401_response(message=u'用户名或密码错误')

        # 验证token
        if access_id_or_token:
            user = self._get_user_from_auth_token(access_id_or_token)
            if not user:
                raise_401_response(message=u'请重新登录')
            # FIXME: 0需要与数据库常量同步
            if (not user) or user.status != 0:
                raise_401_response(message=u'请重新登录')
            g.current_user = user
            g.token_used = True
            return True

        raise_401_response(message=u'请登录')

    def __init__(self, app=None, db=None):
        self.app = app
        self.db = db
        self.auth = HTTPBasicAuth()
        self.auth.error_handler(_unauthorized)
        self.auth.verify_password(self._verify_password)

        if app is not None and db is not None:
            self.init_app(app, db)

    def init_app(self, app, db):
        if app is None:
            raise

        self.app = app
        self.db = db
