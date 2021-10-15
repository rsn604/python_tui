#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

class ListDBSQLite3:
    def __init__(self,  database_connect):
        self.connection = sqlite3.connect(database_connect)
        self.connection.text_factory = str
        self.cursor = self.connection.cursor()

    def get_drop_meta_sql(self):
        return "drop table if exists MetaTable"

    def get_define_sql(self):
        return "CREATE TABLE MetaTable (id INTEGER PRIMARY KEY AUTOINCREMENT, DBName text, fieldName1 text, fieldName2 text, categoryList text)"    

    def get_insert_meta_sql(self):
        return "INSERT INTO MetaTable (DBName, fieldName1, fieldName2, categoryList) VALUES (?, ?, ?, ?)"

    def get_update_meta_sql(self, dbName):
        return "UPDATE MetaTable set fieldName1=?, fieldName2=?, categoryList=? where DBName='"+dbName+"'"

    def get_delete_meta_sql(self, dbName):
       return "DELETE FROM MetaTable where DBName = '"+dbName+"'"

    def get_define_list_sql(self, dbName):
        return "CREATE TABLE '"+dbName+"' (id INTEGER  PRIMARY KEY AUTOINCREMENT, category text, field01 text, field02 text, note text)"

    def get_insert_sql(self, dbName):
        return "INSERT INTO '"+dbName+"' (category, field01, field02, note) VALUES (?, ?, ?, ?)"     

    def get_update_sql(self, dbName):
        return "UPDATE '"+dbName+"' set category=?, field01=?, field02=?, note=? where id="
    def get_delete_sql(self, dbName):
        return "DELETE FROM '"+dbName+"' where id="

    def get_limit_sql(self, countRec, fromRec):
        if countRec >0:
            return " limit "+str(countRec)+" offset "+str(fromRec-1) 
        else:
            return ""

    def get_drop_sql(self, dbName):
        return "drop table if exists '"+dbName+"'"

    def get_qname(self, dbName):
        return "'"+dbName+"'"

    def get_last_rowid(self, dbName):
        return self.cursor.lastrowid

    def get_record_count_sql(self, dbName):
        return "select count(*) from '"+dbName+"'"
    
