#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# load_db.py
#
import os, sys
import time

from listdb.manager import get_manager

def reprDirInfo(dirpath, flist):
    for path in os.listdir(dirpath):
        full = os.path.join(dirpath,path)
        if os.path.isdir(full):
            reprDirInfo(full, flist)
        elif os.path.isfile(full):
            flist.append(full)

def main(database_name, database_connect, csv_dir):
    manager = get_manager(database_name, database_connect)
    manager.define()    
    flist = []
    reprDirInfo(csv_dir, flist)
    for full in flist:
        (root,ext) = os.path.splitext(full)
        if ext.lower()=='.csv':
            ret_code = manager.import_csv(full);
            print ("Loaded "+ full+" ret:"+str(ret_code))            
    manager.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print ("Specify <databese name> <connect string> <CSV dir>")
        sys.exit()

    time1 = time.time()
    main(sys.argv[1], sys.argv[2], sys.argv[3]) 
    time2 = time.time() - time1
    print ('Elapse:'+str(time2) +"sec")


