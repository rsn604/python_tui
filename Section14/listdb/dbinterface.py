#! /usr/bin/env python
# -*- coding: utf-8 -*-

class ListDBInterface:
    def __init__(self, database_name, database_connect):
        if (database_name == "SQLITE3"):
            from . import dbsqlite3
            self.db = dbsqlite3.ListDBSQLite3(database_connect)
        elif (database_name == "MYSQL"):
            from . import dbmysql
            self.db = dbmysql.ListDBMySQL(database_connect)

        self.connection = self.db.connection        
        self.cursor = self.db.cursor        

    # --------------------------------------------------------
    def get_drop_meta_sql(self):
        return self.db.get_drop_meta_sql()
    def get_define_sql(self):
        return self.db.get_define_sql()
    def get_insert_meta_sql(self):
        return self.db.get_insert_meta_sql()
    def get_update_meta_sql(self, dbName):
        return self.db.get_update_meta_sql(dbName)
    def get_delete_meta_sql(self, dbName):
        return self.db.get_delete_meta_sql(dbName)
    def get_define_list_sql(self, dbName):
        return self.db.get_define_list_sql(dbName)
    def get_insert_sql(self, dbName):
        return self.db.get_insert_sql(dbName)
    def get_update_sql(self, dbName):
        return self.db.get_update_sql(dbName)
    def get_delete_sql(self, dbName):
        return self.db.get_delete_sql(dbName)
    def get_limit_sql(self, countRec, fromRec):
        return self.db.get_limit_sql(countRec, fromRec)
    def get_drop_sql(self, dbName):
        return self.db.get_drop_sql(dbName)
    def get_qname(self, dbName):
        return self.db.get_qname(dbName)
    def get_last_rowid(self,dbName):
        return self.db.get_last_rowid(dbName)
    def get_record_count_sql(self, dbName):
        return self.db.get_record_count_sql(dbName)
