#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urwid

import application
import detail

from listwalker import ListWalker
from mywidget import *
from common import Common

from listdb.manager import get_manager

# -------------------------------------------------------
# Main 
# -------------------------------------------------------
class List(application.Application):
    def __init__(self, common=None):
        if common != None:
            self.common = common
        self.listbox = None
        self.is_last = False

    # -------------------------------------------
    # Table
    # -------------------------------------------
    def get_table(self, ignored=None):
        manager = get_manager(self.common.database_name, self.common.database_connect)
        tables = manager.get_db_names()
        tables.sort()
        manager.close()
        my_select_box(self.main_loop, tables, self.common.table_name, u"Tables", self.get_table_name)
        
    def get_table_name(self, button):
        self.common.table_name = button.get_label()
        self.common.reset()
        self.display()
        
    # -------------------------------------------
    # Category
    # -------------------------------------------
    def get_category(self, ignored=None):
        manager = get_manager(self.common.database_name, self.common.database_connect)
        categories = manager.get_category_list(self.common.table_name)
        #categories.sort()
        categories.insert(0, 'Clear')
        manager.close()
        my_select_box(self.main_loop, categories, self.common.category, u"Category list", self.get_category_name)
        
    def get_category_name(self, button):
        self.common.category = button.get_label()
        if self.common.category == 'Clear':
            self.common.category = None
        self.common.reset_paging()
        self.display()

    # -------------------------------------------
    # Search
    # -------------------------------------------
    def get_search(self, ignored=None):
        if self.common.search != None:
            edit = MySearchEdit(edit_text=self.common.search, align="left")
        else:            
            edit = MySearchEdit("", align="left")
        edit.press_enter = self.press_enter

        btn_OK = create_mybutton("OK", self.on_submit, edit)
        btn_Cancel = create_mybutton("Cancel", self.on_submit, edit)
        ok_cancel = urwid.GridFlow([btn_OK, btn_Cancel], 10, 1, 1, 'right')

        pile = [
            urwid.AttrMap(edit, "search", "search"),
            urwid.Divider(),
            urwid.Padding(ok_cancel)
        ]
         
        my_dialog(self.main_loop, urwid.LineBox(urwid.Filler(urwid.Pile(pile)), title=u'Search', title_align='left'), height=7, align=('relative', 40), valign=('relative', 10))

    def on_submit(self, button, edit): 
        if button.get_label() == 'OK':
            self.common.search = edit.get_edit_text()
            self.common.reset_paging()
        if button.get_label() == 'Cancel':
            self.common.search = None
        self.display()

    def press_enter(self, search): 
        self.common.search = search
        self.common.reset_paging()
        self.display()        

    # -------------------------------------------
    # Paging
    # -------------------------------------------
    def next_page(self, ignored=None):
        if not self.last_page():
            self.common.from_rec += self.rows
            self.display()

    def prior_page(self, ignored=None):
        if self.common.from_rec > self.rows:
            self.common.from_rec -= self.rows
            self.display()

    def first_page(self):
        return self.common.from_rec == 1

    def last_page(self):
        return self.is_last

    #---------------------------------------------------
    # Start Detail
    #---------------------------------------------------
    def start_detail(self):
        self.common.selected_item = self.listbox.focus_position + self.common.from_rec
        self.start(detail.Detail, self.common)

    #---------------------------------------------------
    # Double click
    #---------------------------------------------------
    def double_click(self):
        self.start_detail()
        
    #---------------------------------------------------
    # Unhandled keypress
    #---------------------------------------------------
    def unhandled_keypress(self, k):
        if k in ('t', 'T'):
            self.get_table()

        elif k == 'esc':
            self.cols, self.rows = self.get_cols_rows()
            self.display()
            
        elif k in ('q', 'Q'):
            self.exit()        

        # ----------------------------------------------
        if self.common.table_name == None:
            return True
        
        if self.main_loop.widget.focus_position == 'header' and k == 'down':
            self.main_loop.widget.focus_position = 'body'
        elif self.main_loop.widget.focus_position == 'body' and k == 'up':
            self.main_loop.widget.focus_position = 'header'

        elif k == 'enter':
            self.start_detail()

        elif k in ('n', 'N'):
            self.next_page()

        elif k in ('p', 'P'):
            self.prior_page()

        elif k in ('s', 'S'):
            self.get_search()

        elif k in ('c', 'C'):
            self.get_category()
        else:
            return
        return True

    #---------------------------------------------------
    # get "from_rec"
    #---------------------------------------------------
    def get_start_record(self, item):
        if self.common.from_rec >= self.common.selected_item:
            return self.common.from_rec
        '''
        if self.common.from_rec <= self.common.selected_item < self.common.from_rec+self.rows:
            return self.common.from_rec
        '''
        if int(item/self.rows)*self.rows == item:
            return (int(item/self.rows) - 1)*self.rows+1
        else:
            return (int(item/self.rows))*self.rows+1

    #---------------------------------------------------
    # format screen
    #---------------------------------------------------
    def doformat(self):
        self.common.from_rec =  self.get_start_record(self.common.selected_item)
        walker = ListWalker(self.common, self.rows, self.cols)
        self.is_last = walker.last_page()
        self.record_count = walker.get_record_count()
        self.listbox = urwid.ListBox(walker)
        
        # buttons
        btn_table = create_mybutton("T", self.get_table)
        if self.last_page() or self.common.table_name == None:
            btn_next = urwid.Divider()
        else:
            btn_next = create_mybutton("N", self.next_page)
        if self.first_page():            
            btn_prior = urwid.Divider()
        else:
            btn_prior = create_mybutton("P", self.prior_page)
        if self.common.table_name == None:
            btn_category = urwid.Divider()
            btn_search = urwid.Divider()
        else:
            btn_category = create_mybutton("C", self.get_category)
            btn_search = create_mybutton("S", self.get_search)
        btn_exit = create_mybutton("Q", self.exit)

        header = urwid.GridFlow([btn_table, btn_next, btn_prior, btn_category, btn_search, btn_exit], 6, 1, 1, 'left')

        if self.common.table_name != None:
            footer = urwid.AttrWrap(urwid.Text(str(self.common.from_rec)+"/"+str(self.record_count)+" "+self.common.table_name), "foot")
        else:
            footer = urwid.AttrWrap(urwid.Text(""), "foot")

        frame = MyFrame(urwid.AttrWrap(self.listbox, 'body'),
            header=header,
            footer=footer)
        # Double click event
        frame.double_click = self.double_click

        if self.common.table_name != None and self.record_count > 1:
            if self.common.from_rec <= self.common.selected_item < self.common.from_rec+self.rows:
                self.listbox.focus_position = self.common.selected_item - self.common.from_rec
            self.common.selected_item = 0
            frame.focus_position = 'body'
        else:
            frame.focus_position = 'header'
        return frame
    
def main(database_name, database_connect):
    common = Common()
    common.database_name = database_name
    common.database_connect = database_connect
    List.get_instance(common).run()

if __name__=="__main__":
    if len(sys.argv) == 3:
        database_name = sys.argv[1]
        database_connect = sys.argv[2]
    else:
        database_name = 'SQLITE3'
        database_connect = './db/ListDB.sqlite3'
        #database_name = 'MYSQL'
        #database_connect = 'mysql://user01:pass01@localhost/ListDB'
    main(database_name, database_connect)
