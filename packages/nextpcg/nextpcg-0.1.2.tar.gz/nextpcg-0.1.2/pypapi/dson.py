# -*- coding: utf-8 -*-
"""
Author  : NextPCG
"""

from .meta_helper import Singleton
from .const import *


class nextpcgmethod(staticmethod):
    def __init__(self, function):
        super(nextpcgmethod, self).__init__(function)


class DsonMetaInfo:
    def __init__(self, cls_name):
        self.cls_name = cls_name

    def to_json(self):
        return {dson_meta_clsname_tag: self.cls_name}

    @staticmethod
    def from_json(json_data):
        return DsonMetaInfo(json_data[dson_meta_clsname_tag])


class DsonManager(metaclass=Singleton):
    def __init__(self):
        self.dsonMap = {}


class DsonMeta(type):
    def __init__(cls, *args, **kwargs):
        assert hasattr(cls, 'label')
        DsonManager().dsonMap[cls.__name__] = cls
        super().__init__(*args, **kwargs)


class DsonBase(metaclass=DsonMeta):
    label = "pda"

    def __init__(self):
        pass
