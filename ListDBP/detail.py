#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urwid
import sys
import webbrowser
import subprocess
import re
import math

import application
import list
from mywidget import *
from common import Common

from listdb.manager import get_manager, get_listdata

# -------------------------------------------------------
# Main
# -------------------------------------------------------
class Detail(application.Application):

    def __init__(self, common=None):
        if common != None:
            self.common = common

    # -------------------------------------------
    # Return to main
    # -------------------------------------------
    '''
    def get_start_record(self, item):
        if int(item/self.rows)*self.rows == item:
            return (int(item/self.rows) - 1)*self.rows+1
        else:
            return (int(item/self.rows))*self.rows+1
    '''
    def return_main(self, ignored=None):
        # python2.7 does not work expected .
        #self.common.from_rec = (math.ceil(self.common.selected_item/self.rows) - 1)*self.rows+1
        #self.common.from_rec =  self.get_start_record(self.common.selected_item)
        self.start(list.List, self.common)

    # -------------------------------------------
    # Messagebox :confirm update, delete, insert
    # -------------------------------------------
    def update(self, ignored=None):
        my_message_box(self.main_loop, u'Update record ?', self.go_update)

    def delete(self, ignored=None):
        my_message_box(self.main_loop, u'Delete record ?', self.go_delete)

    def insert(self, ignored=None):
        my_message_box(self.main_loop, u'Insert record ?', self.go_insert)

    # -------------------------------------------
    # Update , Delete, Insert
    # -------------------------------------------
    def create_listdata(self):
        return get_listdata(self.id, self.btn_category.base_widget.get_label(), self.edit_field01.base_widget.get_edit_text(), self.edit_field02.base_widget.get_edit_text(), self.edit_note.base_widget.get_edit_text())
    
    def go_update(self, button):
        if button.get_label() == 'OK':
            manager = get_manager(self.common.database_name, self.common.database_connect)

            listdb = manager.update(self.common.table_name, self.id, self.create_listdata())
            manager.close()
        self.display()

    def go_delete(self, button):
        if button.get_label() == 'OK':
            manager = get_manager(self.common.database_name, self.common.database_connect)

            listdb = manager.delete(self.common.table_name, self.id)
            manager.close()
        self.common.reset_paging()
        self.return_main()

    def go_insert(self, button):
        if button.get_label() == 'OK':
            manager = get_manager(self.common.database_name, self.common.database_connect)
            listdb = manager.insert(self.common.table_name, self.create_listdata())
            manager.close()
        self.common.reset_paging()
        self.return_main()

    # -------------------------------------------
    # Paging
    # -------------------------------------------
    def next_page(self, ignored=None):
        if self.is_last == False:
            self.common.selected_item += 1
            self.display()

    def prior_page(self, ignored=None):
        if self.common.selected_item > 1:
            self.common.selected_item -= 1
            self.display()

    def first_page(self):
        return self.common.selected_item == 1

    def last_page(self):
        return self.is_last

    # ---------------------------------------------------
    # Unhandled keypress
    # ---------------------------------------------------
    def unhandled_keypress(self, k):
        if self.main_loop.widget.focus_position == 'header' and k == 'down':
            self.main_loop.widget.focus_position = 'body'
        elif self.main_loop.widget.focus_position == 'body' and k == 'up':
            self.main_loop.widget.focus_position = 'header'
        elif self.main_loop.widget.focus_position == 'body' and k == 'down':
            self.main_loop.widget.focus_position = 'footer'
        elif self.main_loop.widget.focus_position == 'footer' and k == 'up':
            self.main_loop.widget.focus_position = 'body'
        elif self.main_loop.widget.focus_position == 'footer' and k == 'down':
            self.main_loop.widget.focus_position = 'header'

        elif k in ('q', 'Q'):
            self.exit()

        elif k in ('r', 'R'):
            self.return_main()

        elif k in ('n', 'N'):
            self.next_page()

        elif k in ('p', 'P'):
            self.prior_page()

        elif k in ('u', 'U'):
            self.update()

        elif k in ('d', 'D'):
            self.delete()

        elif k in ('i', 'I'):
            self.insert()

        else:
            return
        return True

    # ---------------------------------------------------
    # Invoke URL
    # ---------------------------------------------------
    def invoke_url(self, button):
        webbrowser.open(button.get_label())

    # ---------------------------------------------------
    # Invoke Browser and open Google Maps
    # ---------------------------------------------------
    def invoke_browser_maps(self, button, edit_field):
        try:
            webbrowser.open("http://maps.google.co.jp/maps?q=" + edit_field.original_widget.get_edit_text())
        except webbrowser.Error:
            return

    # ---------------------------------------------------
    # Invoke Google Maps by intent
    # ---------------------------------------------------
    def invoke_google_maps(self, button, edit_field):
        try:
            cmd = "am start -a android.intent.action.VIEW -d geo:0,0?q="+edit_field.original_widget.get_edit_text()
            subprocess.run(cmd.split())
        except FileNotFoundError:
            return

    # ---------------------------------------------------
    # Map fields
    # ---------------------------------------------------
    def set_field_intent(self, field_name, edit_field):
        import distutils.spawn
        if field_name.lower() in ['address', 'map']:
            if distutils.spawn.find_executable('am') != None:
                field = create_mybutton(field_name+" -> Intent(GooleMaps)", self.invoke_google_maps, edit_field)
            else:
                field = create_mybutton(field_name+" -> Browser(GooleMaps)", self.invoke_browser_maps, edit_field)
        else:
            field = create_mylabel(field_name)
        return field

    # ---------------------------------------------------
    # Extract URLS and create button
    # ---------------------------------------------------
    def get_urls(self, text):
        url_list = []
        urls = re.findall(r'("https?://\S+")', text)
        for url in urls:
            url_list.append(create_mybutton(url.strip('"'), self.invoke_url))
        return url_list

    # -------------------------------------------
    # Category
    # -------------------------------------------
    def get_category(self, ignored=None):
        manager = get_manager(self.common.database_name, self.common.database_connect)
        categories = manager.get_category_list(self.common.table_name)
        categories.sort()
        manager.close()
        self.parent = self.main_loop.widget
        my_select_box(self.main_loop, categories, self.common.category, u"Category list", self.get_category_name)
        
    def get_category_name(self, button):
        self.btn_category.original_widget.set_label(button.get_label())
        self.main_loop.widget = self.parent

    # ---------------------------------------------------
    # Detail body
    # ---------------------------------------------------
    def detail_body(self, common):
        self.is_last = False
        manager = get_manager(self.common.database_name, self.common.database_connect)
        listdb = manager.search_db(
            common.table_name, common.category, common.search, self.common.selected_item, 2)
        if len(listdb.listData) < 2:
            self.is_last = True
        manager.close()
        self.id = listdb.listData[0].id
        self.btn_category = create_mybutton(listdb.listData[0].category, self.get_category)
        self.edit_field01 = create_myedit(listdb.listData[0].field01)
        self.edit_field02 = create_myedit(listdb.listData[0].field02)
        self.edit_note = create_myedit(listdb.listData[0].note, multiline=True)
        pile = [
            create_mylabel(u'ID'),
            urwid.Text(str(self.id), align="left"),
            create_mylabel(u'Category'),
            self.btn_category,
            self.set_field_intent(listdb.fieldName01, self.edit_field01),
            self.edit_field01,
            self.set_field_intent(listdb.fieldName02, self.edit_field02),
            self.edit_field02,
            create_mylabel(u'Note'),
            self.edit_note
        ]
        pile.extend(self.get_urls(listdb.listData[0].note))
        return urwid.Pile(pile)

    # ---------------------------------------------------
    # Format screen
    # ---------------------------------------------------
    def doformat(self):
        body = urwid.Filler(self.detail_body(self.common), valign='top')

        btn_return = create_mybutton("R", self.return_main)
        if self.last_page():
            btn_next = urwid.Divider()
        else:
            btn_next = create_mybutton("N", self.next_page)
        if self.first_page():
            btn_prior = urwid.Divider()
        else:
            btn_prior = create_mybutton("P", self.prior_page)
        btn_exit = create_mybutton("Q", self.exit)
        header = urwid.GridFlow([btn_return, btn_next, btn_prior, urwid.Divider(
), urwid.Divider(), btn_exit], 6, 1, 1, 'left')

        btn_update = create_mybutton("U", self.update)
        btn_delete = create_mybutton("D", self.delete)
        btn_insert = create_mybutton("I", self.insert)
        footer = urwid.GridFlow(
            [btn_update, btn_delete, btn_insert], 6, 1, 1, 'left')
        frame = urwid.Frame(urwid.AttrWrap(body, 'body'),
                           header=header,
                           footer=footer)
        frame.focus_position = 'header'
        return frame

def main(database_name, database_connect):
    common = Common()
    common.database_name = database_name
    common.database_connect = database_connect
    common.table_name = 'BookOf'
    Detail.get_instance(common).run()

if __name__ == "__main__":
    main('SQLITE3', './db/ListDB.sqlite3')
