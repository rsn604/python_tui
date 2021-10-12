#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys, codecs
import csv

from . import listdb as ListDB
from . import listdata as ListData

def to_unicode(text, charset='utf-8'):
    ### python 2-3
    if sys.version_info[0] == 2:
        if isinstance(text, str):
            return text.decode(charset)
        else:
            return text
    elif sys.version_info[0] == 3:
        return text

def to_str(text, charset='utf-8'):
    ### python 2-3
    if sys.version_info[0] == 2:
        if isinstance(text, unicode):
            return text.encode(charset)
        else:
            return text
    
    elif sys.version_info[0] == 3:
        return text

def concate_data(flds, flag):
    return flag.join(flds)

def concate_data2(flds, flag):
    # delete "" and goto string.
    return concate_data(list(filter(None, flds)), flag)
    """
    notes = ""
    for fld in flds:
        if fld != "":
            notes=notes+fld+flag
    return notes[:-1]
    """
def get_db_names(db):
    db_names = []
    db.cursor.execute("select * from MetaTable")
    rows = db.cursor.fetchall()
    for row in rows:
        db_names.append(to_unicode(row[1]))
    return db_names

def get_category_list(db, db_name):
    db.cursor.execute("select * from MetaTable where DBName ='"+db_name+"'")
    row = db.cursor.fetchone()
    return to_unicode(row[4]).split(',')

def get_data(db, listdb, sql_value, from_rec, count_rec):
    qs_sql = "select id, category, field01, field02, note from "+db.get_qname(listdb.dbName)+" "

    if (sql_value != None):
        qs_sql = qs_sql + to_unicode(sql_value)

    qs_sql = qs_sql + db.get_limit_sql(count_rec, from_rec) ;
    db.cursor.execute(qs_sql+"");

    rec = 1
    while True:
        row = db.cursor.fetchone()
        if row == None:
            break
        if (count_rec>0) and (rec>count_rec):
            break
        listdb.add_listdata(ListData.ListData(to_unicode(row[0]), to_unicode(row[1]), to_unicode(row[2]), to_unicode(row[3]), to_unicode(row[4])))
        rec = rec + 1
    return listdb ;

def get_meta_table(db, sql):
    db.cursor.execute(sql)
    row = db.cursor.fetchone()
    listdb = ListDB.ListDB(to_unicode(row[0]), to_unicode(row[1]), to_unicode(row[2]), to_unicode(row[3]), to_unicode(row[4]))
    return listdb 

def get_db(db, db_name,  sql_value,  from_rec,  count_rec):
    sql = "select * from MetaTable where DBName ='"+db_name+"'";
    listdb = get_meta_table(db, sql) 
    return get_data(db, listdb, sql_value, from_rec, count_rec) ;

def get_db_by_id(db, id,  sql_value,  from_rec,  count_rec):
    sql = "select * from MetaTable where id = "+str(id)+"";
    listdb = get_meta_table(db, sql) ;
    return get_data(db, listdb, sql_value, from_rec, count_rec) ;

def get_data_by_id(db, db_name, id):
    sql = "select * from MetaTable where DBName ='"+db_name+"'";
    listdb = get_meta_table(db, sql) 
    sql_Value = "where id = "+str(id)
    return get_data(db, listdb, sql_Value, 1, 1) ;

def get_csv_data(fname):
    ### python 2-3
    if sys.version_info[0] == 2:
        f  = codecs.open(fname, 'r')
    else:
        f  = codecs.open(fname, 'r', encoding="utf-8")

    for row in csv.reader(f,  delimiter=',', quotechar='"'):
        #for row in csv.reader(f,  delimiter=',', quoting=csv.QUOTE_NONE):
        yield row
    f.close()

def delete_list(db, db_name):
    try:
        db.cursor.execute(db.get_drop_sql(db_name))                    
    except:
        pass

def define_list(db, db_name):
    delete_list(db, db_name);                    
    db.cursor.execute(db.get_define_list_sql(db_name))

def delete_data(db, db_name, id):
    db.cursor.execute(db.get_delete_sql(db_name)+str(id))

def update_data(db, db_name, id, fields):
    db.cursor.execute(db.get_update_sql(db_name)+str(id), (to_str(fields[0]), to_str(fields[1]), to_str(fields[2]), to_str(concate_data(fields[3:],'\n'))))

def insert_data(db, db_name, fields):
    db.cursor.execute(db.get_insert_sql(db_name), (to_str(fields[0]), to_str(fields[1]), to_str(fields[2]), to_str(concate_data(fields[3:],'\n'))))
    return db.get_last_rowid(db_name)

def insert_meta(db, fields):
    if (len(fields) <4):
        return False
    try:
        db.cursor.execute(db.get_delete_meta_sql(fields[0]))
    except:
        pass
    db.cursor.execute(db.get_insert_meta_sql(), (to_str(fields[0]), to_str(fields[1]), to_str(fields[2]), to_str(concate_data2(fields[3:],','))))
    return True

'''
def import_json(db, js):
    listdb = ListDB.ListDB.json2obj(js)
    fields = []
    fields.append(listdb.dbName)
    fields.append(listdb.fieldName01) 
    fields.append(listdb.fieldName02) 
    category_list = listdb.categoryList.split(',')
    for category in category_list:
        if len(category) > 0:
            fields.append(category) 
    ret_code = insert_meta(db, fields)
    if (ret_code == False):
        raise Exception("D.ER listdb_util:insert_meta error")

    for i in range(len(listdb.listData)):
        listdata = ListData.ListData(i, listdb.listData[i].category, listdb.listData[i].field01, listdb.listData[i].field02, listdb.listData[i].note)
        insert_data(db, listdb.dbName, listdata.to_list())
    return True
'''
def import_csv(db, fname):
    first_time = True
    ret_code = True

    for fields in get_csv_data(fname):
        if (len(fields)==0):
            continue
        if (first_time == True):
            ret_code = insert_meta(db, fields)
            if (ret_code == False):
                raise Exception("D.ER listdb_util:insert_meta error")
            db_name = fields[0]
            define_list(db, db_name);                    
            first_time = False
        else:
            insert_data(db, db_name, fields)
    return ret_code

def define(db):
    try:
        db.cursor.execute(db.get_drop_meta_sql())
    except:
        pass

    db.cursor.execute(db.get_define_sql())

def close(db):
    db.cursor.close()
    db.connection.close()

def get_record_count(db, db_name, sql_value=None):
    sql = db.get_record_count_sql(db_name)
    if sql_value != None:
        #sql = sql + sql_value
        sql = sql + to_unicode(sql_value)
    db.cursor.execute(sql)
    row = db.cursor.fetchone()
    return row[0]
