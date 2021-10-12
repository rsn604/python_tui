#! /usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import print_function
try:
    import psycopg2
except ImportError, err:
    print ('D.MG psycopg2 cannot be imported: ignore if not used.', err)
    pass

from . import urlanalyze

class ListDBPostgres:
    def __init__(self,  connect_string):
        u = urlanalyze.UrlAnalyze(connect_string)
        if (u.port == None):
            self.connection = psycopg2.connect(host=u.hostname, database=u.db_name, user=u.username, password=u.password)
        else:
            self.connection = psycopg2.connect(host=u.hostname, port=u.port, database=u.db_name, user=u.username, password=u.password)
        self.cursor = self.connection.cursor()

    # ---------------------------------------------------------
    def get_drop_meta_sql(self):
        return "drop table if exists MetaTable"

    def get_define_sql(self):
        return "CREATE TABLE MetaTable (id SERIAL PRIMARY KEY , DBName text, fieldName1 text, fieldName2 text, categoryList text)"

    def get_insert_meta_sql(self):
        return "INSERT INTO MetaTable (DBName, fieldName1, fieldName2, categoryList) VALUES (%s, %s, %s, %s)"

    def get_update_meta_sql(self, dbName):
        return "UPDATE MetaTable set fieldName1=%s, fieldName2=%s, categoryList=%s where DBName=\""+dbName+"\""

    def get_delete_meta_sql(self, dbName):
       return "DELETE FROM MetaTable where DBName = '"+dbName+"'"

    def get_define_list_sql(self, dbName):
        return "CREATE TABLE \""+dbName+"\" (id SERIAL PRIMARY KEY , category text, field01 text, field02 text, note text)"

    def get_insert_sql(self, dbName):
        return "INSERT INTO \""+dbName+"\" (category, field01, field02, note) VALUES (%s, %s, %s, %s)" 

    def get_update_sql(self, dbName):
        return "UPDATE \""+dbName+"\" set category=%s, field01=%s, field02=%s, note=%s where id="
    def get_delete_sql(self, dbName):
        return "DELETE FROM \""+dbName+"\" where id="

    def get_limit_sql(self, countRec, fromRec):
        if countRec >0:
            return " limit "+str(countRec)+" offset "+str(fromRec-1) 
        else:
            return ""

    def get_drop_sql(self, dbName):
        return "drop table if exists \""+dbName+"\""

    def get_qname(self, dbName):
        return "\""+dbName+"\""

    def get_last_rowid(self, dbName):
        self.cursor.execute("SELECT LASTVAL()")
        return self.cursor.fetchone()[0]

    def get_record_count_sql(self, dbName):
        return "select count(*) from \""+dbName+"\""
