#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# list.py
#
import urwid

import application  
import list
from mywidget import *
from common import Common

class Detail(application.Application):  
    def __init__(self, common):
        self.common = common
        self.is_last = False
        
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

    def unhandled_keypress(self, k):
        if self.main_loop.widget.focus_position == 'header' and k == 'down':
            self.main_loop.widget.focus_position = 'body'
        elif self.main_loop.widget.focus_position == 'body' and k == 'up':
            self.main_loop.widget.focus_position = 'header'

        if k in ('q', 'Q'):
            self.exit()        
        elif k in ('r', 'R'):
            self.return_main()
        elif k in ('n', 'N'):
            self.next_page()
        elif k in ('p', 'P'):
            self.prior_page()
        else:
            return
        return True

    def doformat(self, from_rec=1):
        items = get_items(self.common.table_name)
        self.edit_field01 = create_myedit(items[self.common.selected_item-1][0])
        self.edit_field02 = create_myedit(items[self.common.selected_item-1][1])
        self.edit_note = create_myedit(items[self.common.selected_item-1][2],multiline=True)
        pile = [
            create_mylabel("Field01"),
            self.edit_field01,
            create_mylabel("Field02"),
            self.edit_field02,
            create_mylabel("Note"),
            self.edit_note
        ]
        body = urwid.Filler(urwid.Pile(pile), valign='top')
        if self.common.selected_item == len(items):
            self.is_last = True
        
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

        self.footer_text = urwid.Text(u"これはフッター")
        footer = urwid.AttrWrap(self.footer_text, "foot")

        frame = MyFrame(urwid.AttrWrap(body, 'body'), header=header, footer=footer)
        frame.focus_position = 'header'
        return frame 

    def return_main(self, ignored=None):
        self.start(list.List, self.common)

def main():
    common = Common()
    Detail(common).run()

if __name__=="__main__":
    main()
