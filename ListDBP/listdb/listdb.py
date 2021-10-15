#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json 
from collections import namedtuple
from . import listdata as ListData

class ListDB:
    def __init__(self, id, dbName, fieldName01, fieldName02, categoryList):
        self.id=id
        self.dbName=dbName
        self.fieldName01=fieldName01
        self.fieldName02=fieldName02
        self.categoryList=categoryList
        self.listData = []

    def add_listdata(self, listData): 
        self.listData.append(listData)

    def get_listdata(self): 
        return self.listData

    def count_listdata(self): 
        return len(self.listData)

    def __str__(self):
       return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def _default_encode(self, obj):
        if isinstance(obj, ListData.ListData):
            return obj.__dict__
        return obj

    def obj2json(self): 
        return json.dumps(self.__dict__, ensure_ascii=False, default=self._default_encode)

    @staticmethod
    def _json_object_hook(d):
        return namedtuple('X', d.keys())(*d.values())

    @staticmethod
    def json2obj(data): 
        x = json.loads(data, object_hook=ListDB._json_object_hook)
        listdb = ListDB(x.id, x.dbName, x.fieldName01, x.fieldName02, x.categoryList)
        for i in range(len(x.listData)):
            listdata = ListData.ListData(i, x.listData[i].category, x.listData[i].field01, x.listData[i].field02, x.listData[i].note)
            listdb.add_listdata(listdata)
        return listdb 

