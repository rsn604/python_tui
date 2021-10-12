#! /usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import print_function
try:
    import pymysql as MySQLdb
    #import MySQLdb

except ImportError as err:
    print ('D.MG MySQLdb cannot be imported: ignore if not used', err)
    pass

b_use_unicode = True
from . import urlanalyze
from warnings import filterwarnings
class ListDBMySQL:
    def __init__(self,  connect_string):
        u = urlanalyze.UrlAnalyze(connect_string)
        if (u.port == None):
            self.connection = MySQLdb.connect(host=u.hostname, db=u.db_name, user=u.username, passwd=u.password, charset='utf8', use_unicode=b_use_unicode)
        else:
            self.connection = MySQLdb.connect(host=u.hostname, port=u.port, db=u.db_name, user=u.username, passwd=u.password, charset='utf8', use_unicode=b_use_unicode)

        self.cursor = self.connection.cursor()
        filterwarnings('ignore', category = MySQLdb.Warning)

    # -----------------------------------------------------------
    def get_drop_meta_sql(self):
        return "drop table if exists MetaTable"

    def get_define_sql(self):
        return "CREATE TABLE MetaTable (id INTEGER PRIMARY KEY AUTO_INCREMENT , DBName text, fieldName1 text, fieldName2 text, categoryList text)" 

    def get_insert_meta_sql(self):
        return "INSERT INTO MetaTable (DBName, fieldName1, fieldName2, categoryList) VALUES (%s, %s, %s, %s)"

    def get_update_meta_sql(self, dbName):
        return "UPDATE MetaTable set fieldName1=%s, fieldName2=%s, categoryList=%s where DBName=`"+dbName+"`"

    def get_delete_meta_sql(self, dbName):
       return "DELETE FROM MetaTable where DBName = '"+dbName+"'"

    def get_define_list_sql(self, dbName):
        return "CREATE TABLE `"+dbName+"` (id INTEGER  PRIMARY KEY AUTO_INCREMENT, category text, field01 text, field02 text, note text)"

    def get_insert_sql(self, dbName):
        return "INSERT INTO `"+dbName+"` (category, field01, field02, note) VALUES (%s, %s, %s, %s)" 

    def get_update_sql(self, dbName):
        return "UPDATE `"+dbName+"` set category=%s, field01=%s, field02=%s, note=%s where id="

    def get_delete_sql(self, dbName):
        return "DELETE FROM `"+dbName+"` where id="

    def get_limit_sql(self, countRec, fromRec):
        if countRec >0:
            return " limit "+str(countRec)+" offset "+str(fromRec-1) 
        else:
            return ""

    def get_drop_sql(self, dbName):
        return "drop table if exists `"+dbName+"`"

    def get_qname(self, dbName):
        return "`"+dbName+"`"

    def get_last_rowid(self, dbName):
        return self.cursor.lastrowid

    def get_record_count_sql(self, dbName):
        return "select count(*) from `"+dbName+"`"
