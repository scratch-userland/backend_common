# -*- coding: utf-8 -*-
import datetime


class BaseService(object):
    """Base service to inherit from."""
    pass


class ModelService(BaseService):
    """Model service"""

    _model = None

    def __init__(self, obj=None):
        """
        Takes model instance
        :param obj: model instance
        """
        self._obj = None

        if isinstance(obj, self._model):
            self._obj = obj

    def get_object_or_none(self, **lookup):
        """Get object using lookup parameters, i.e pk=1"""
        if lookup:
            self._obj = self._model.query.filter_by(**lookup).first()
        return self._obj or None

    def get_objects_all(self, **lookup):
        if lookup:
            return self._model.query.filter_by(**lookup).all()

    @classmethod
    def create(cls, **data):
        return cls._model.create(**data)

    @classmethod
    def update(cls, id, **data):
        _obj = cls.get_by_id(id)
        if _obj:
            return _obj.update(**data)
        else:
            return None

    @classmethod
    def get_by_id(cls, obj_id):
        _obj = cls._model.query.filter_by(id=obj_id).first()
        return _obj or None

    @classmethod
    def delete_by_id(cls, obj_id, commit=False):
        _obj = cls._model.query.filter_by(id=obj_id).first()
        if _obj:
            return _obj.update(commit, active=False, updated_at=datetime.datetime.now())
