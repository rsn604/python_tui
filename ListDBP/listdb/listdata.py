#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json 
from collections import namedtuple

class ListData:
    def __init__(self, id, category, field01, field02, note):
        self.id=id
        self.category=category
        self.field01=field01
        self.field02=field02
        self.note=note

    def to_list(self):
        dim = []
        dim.append(self.category)
        dim.append(self.field01)
        dim.append(self.field02)
        dim.append(self.note)
        return dim


    def __str__(self):
       return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def _default_encode(self, obj):
        return obj

    def obj2json(self): 
        return json.dumps(self.__dict__, ensure_ascii=False, default=self._default_encode)

    @staticmethod
    def _json_object_hook(d): 
        return namedtuple('X', d.keys())(*d.values())

    @staticmethod
    def json2obj(data): 
        x = json.loads(data, object_hook=ListData._json_object_hook)
        listdata = ListData(0, x.category, x.field01, x.field02, x.note)
        return listdata



