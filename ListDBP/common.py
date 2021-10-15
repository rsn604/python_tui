#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Common:
    database_name = None
    database_connect = None
    table_name = None
    category = None
    search = None
    from_rec = 1
    selected_item = 1
    def reset_paging(self):
        self.from_rec = 1
        self.selected_item = 1

    def reset(self):
        self.search = None
        self.category = None
        self.reset_paging()
