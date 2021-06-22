#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# list.py
#
import urwid
from listwalker import ListWalker
from mywidget import *

class List:
    main_loop = None
    from_rec = 1
    
    def __init__(self):
        pass

    def exit(self, button=None):
        raise urwid.ExitMainLoop()

    def get_cols_rows(self):
        cols, rows = urwid.raw_display.Screen().get_cols_rows()
        return cols, rows-2

    def select_list(self):
        focus_widget, idx = self.listbox.get_focus()
        self.footer_text.set_text("pos:"+str(idx)+" data:"+focus_widget.base_widget.text)

    def next_page(self, ignored=None):
        if not self.last_page():
            self.from_rec += self.rows
            self.main_loop.widget = self.doformat()

    def prior_page(self, ignored=None):
        if self.from_rec > self.rows:
            self.from_rec -= self.rows
            self.main_loop.widget = self.doformat()

    def first_page(self):
        return self.from_rec == 1

    def last_page(self):
        return self.is_last
    
    def unhandled_keypress(self, k):
        if self.main_loop.widget.focus_position == 'header' and k == 'down':
            self.main_loop.widget.focus_position = 'body'
        elif self.main_loop.widget.focus_position == 'body' and k == 'up':
            self.main_loop.widget.focus_position = 'header'

        if k in ('q', 'Q'):
            self.exit()        
        elif k in ('n', 'N'):
            self.next_page()
        elif k in ('p', 'P'):
            self.prior_page()
        elif k == 'enter':
            self.select_list()
        else:
            return
        return True

    def doformat(self):
        self.cols, self.rows = self.get_cols_rows()
        walker = ListWalker(get_items(), self.from_rec, self.rows)
        self.is_last = walker.last_page()
        self.listbox = urwid.ListBox(walker)

        if self.last_page():
            btn_next = urwid.Divider()
        else:
            btn_next = create_mybutton("N", self.next_page)
        if self.first_page():            
            btn_prior = urwid.Divider()
        else:
            btn_prior = create_mybutton("P", self.prior_page)

        btn_q = create_mybutton("Q", self.exit)
        header = urwid.GridFlow([btn_next, btn_prior, btn_q], 6, 1, 1, 'left')

        self.footer_text = urwid.Text(u"これはフッター")
        footer = urwid.AttrWrap(self.footer_text, "foot")

        #frame = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'), header=header, footer=footer)
        frame = MyFrame(urwid.AttrWrap(self.listbox, 'body'), header=header, footer=footer)
        frame.double_click = self.select_list
        frame.focus_position = 'header'
        return frame 

    def run(self):
        self.main_loop = urwid.MainLoop(self.doformat(), my_palette, unhandled_input=self.unhandled_keypress)
        self.main_loop.run()

def main():
    List().run()

if __name__=="__main__":
    main()
