#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urwid
import unicodedata

from mywidget import MyText

from listdb.manager import get_manager

class ListWalker(urwid.ListWalker):
    def __init__(self, common, rows, cols):
        self.focus = 0
        self.create_page(common, rows, cols)

    def get_length(self, text):
        count = 0
        for c in text:
            if unicodedata.east_asian_width(c) in 'FWA':
                count += 2
            else:
                count += 1
        return count

    def get_fields_info(self, listData, cols):
        max_field_length = 0
        fields_length = []
        for result in listData:      
            field_length = self.get_length(result.field01)
            if field_length > max_field_length:
                max_field_length = field_length
            fields_length.append(field_length)
        if max_field_length > cols:
            max_field_length = cols

        return max_field_length, fields_length
    
    def create_page(self, common, rows, cols):
        self.lines = []
        self.record_count = 0 
        cols_length = []
        self.is_last = False
        if common.table_name != None:
            manager = get_manager(common.database_name, common.database_connect)
            listdb = manager.search_db(common.table_name, common.category, common.search, common.from_rec, rows+1)
            self.record_count = manager.get_record_count(common.table_name, common.category, common.search)
            manager.close()

            if len(listdb.listData) <= rows:
                self.is_last = True

            max_field_length, fields_length = self.get_fields_info(listdb.listData, cols)
            i = 0
            for result in listdb.listData:
                text = MyText(result.field01+(' '*(max_field_length-fields_length[i]))+' '+result.field02, wrap='clip')
                self.lines.append(urwid.AttrMap(text, None, 'listwalker'))
                i += 1
                if i == rows:
                    break
        
    def last_page(self):
        return self.is_last
    
    def get_record_count(self):
        return self.record_count
    
    def get_focus(self):
        return self.get_at_pos(self.focus)

    def set_focus(self, focus):
        self.focus = focus
        self._modified()

    def get_next(self, start):
        return self.get_at_pos(start + 1)

    def get_prev(self, start):
        return self.get_at_pos(start - 1)

    def get_at_pos(self, pos):
        if pos < 0:
            return None, None

        if len(self.lines) > pos:
            return self.lines[pos], pos
        return None, None

