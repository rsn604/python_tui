#! /usr/bin/env python
# -*- coding: utf-8 -*-
#import json
from . import dbutils

class ListDBManager:
    def __init__(self, db):
        self.db = db

    def get_db_names(self):
        return dbutils.get_db_names(self.db)

    def get_category_list(self, db_name):
        return dbutils.get_category_list(self.db, db_name)
    
    def get_data(self, listdb, sql_value, from_rec, count_rec):
        return dbutils.get_data(self.db, listdb, sql_value, from_rec, count_rec)

    def get_meta_table(self, sql):
        return dbutils.get_meta_table(self.db, sql)

    def create_sql(self, category, search):
        sql = None
        if search != None:
            sql = " where (field01 like " + "'%" + search + "%'"
            sql += " or field02 like " + "'%" + search + "%'"
            sql += " or note like " + "'%" + search + "%')"
        if category != None:
            if sql == None:
                sql = "where (category = '" + category + "')"
            else:
                sql = sql + " and (category = '" + category + "')"
        return sql

    def get_db(self, db_name, sql_value=None, from_rec=1, count_rec=0):
        return dbutils.get_db(self.db, db_name, sql_value, from_rec, count_rec)

    def search_db(self, db_name,  category=None, search=None, from_rec=1, count_rec=0):
        sql_value = self.create_sql(category, search)
        return self.get_db(db_name, sql_value, from_rec, count_rec)

    def get_db_by_id(self, id,  sql_value=None,  from_rec=1,  count_rec=0):
        return dbutils.get_db_by_id(self.db, id,  sql_value,  from_rec,  count_rec)

    def get_data_by_id(self, db_name, id):
        return dbutils.get_data_by_id(self.db, db_name, id)

    def delete(self, db_name, id):
        dbutils.delete_data(self.db, db_name, id)
        self.db.connection.commit()

    def update(self, db_name, id, listdata):
        dbutils.update_data(self.db, db_name, id, listdata.to_list())
        self.db.connection.commit()
        return self.get_data_by_id(db_name, id)

    def insert(self, db_name, listdata):
        lastrowid = dbutils.insert_data(self.db, db_name, listdata.to_list())
        listdata.id = lastrowid
        self.db.connection.commit()
        return lastrowid

    def define(self):
        dbutils.define(self.db)
        self.db.connection.commit()

    def import_csv(self, fname):
        ret_code = dbutils.import_csv(self.db, fname)
        self.db.connection.commit()
        return ret_code

    '''
    def import_json(self, js):
        ret_code = dbutils.import_json(self.db, js)
        self.db.connection.commit()
        return ret_code

    def get_split_token(self, tokens, quote, delim):
        dest = ''
        for token in tokens.splitlines() :
            dest = dest+quote+token+quote+delim
        return dest

    def export_csv(self, db_name, fname, delim=',', quote=''):
        listdb = self.get_db(db_name)
        f=open(fname, 'w')
        f.write(quote+listdb.dbName+quote+delim+quote+listdb.fieldName01+quote+delim+quote+listdb.fieldName02+quote+delim+quote+listdb.categoryList+quote+delim+'\n')
        for listdata in listdb.get_listdata():
            f.write(quote+listdata.category+quote+delim+quote+listdata.field01+quote+delim+quote+listdata.field02+quote+delim+quote+self.get_split_token(listdata.note, quote, delim)+'\n')
        f.close()
        self.db.connection.commit()

    def export_json(self, db_name, fname):
        listdb =  self.get_db(db_name)
        f=open(fname, 'w')
        f.write(listdb.obj2json())
        f.close()
        self.db.connection.commit()
    '''
    
    def close(self):
        dbutils.close(self.db)

    #def get_record_count(self, db_name, sql_value=None):
    def get_record_count(self, db_name, category=None, search=None):
        return dbutils.get_record_count(self.db, db_name, self.create_sql(category, search))

    def get_record_count2(self, db_name, sql_value=None):
        return dbutils.get_record_count(self.db, db_name, sql_value)
