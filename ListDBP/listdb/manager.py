#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

#from . import dbmanager
from . import dbmanager
from . import dbinterface
from . import listdb
from . import listdata

def get_manager(database_name, database_connect):
    manager = dbmanager.ListDBManager(dbinterface.ListDBInterface(database_name, database_connect))
    return manager

def get_listdata(id, category, field01, field02, note):
    return listdata.ListData(id, category, field01, field02, note)
