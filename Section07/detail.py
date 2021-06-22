#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# detail.py
#
import urwid

import application
import list
from mywidget import *

class Detail(application.Application):
    def __init__(self):
        pass
    def unhandled_keypress(self, k):
        if self.main_loop.widget.focus_position == 'header' and k == 'down':
            self.main_loop.widget.focus_position = 'body'
        elif self.main_loop.widget.focus_position == 'body' and k == 'up':
            self.main_loop.widget.focus_position = 'header'

        if k in ('q', 'Q'):
            self.exit()        
        elif k in ('r', 'R'):
            self.return_main()
        else:
            return
        return True
    def doformat(self):
        btn_return = create_mybutton("R", self.return_main)
        btn_q = create_mybutton("Q", self.exit)
        header = urwid.GridFlow([btn_return, btn_q], 6, 1, 1, 'left')

        self.edit_field01 = create_myedit("入力データ その1")
        self.edit_field02 = create_myedit("入力データ その2")
        self.edit_note = create_myedit("改行を含む入力データ\n2行目のデータ\n3行目のデータ",multiline=True)
        pile = [
            create_mylabel("Field01"),
            self.edit_field01,
            create_mylabel("Field02"),
            self.edit_field02,
            create_mylabel("Note"),
            self.edit_note
        ]
        body = urwid.Filler(urwid.Pile(pile), valign='top')

        self.footer_text = urwid.Text(u"これはフッター")
        footer = urwid.AttrWrap(self.footer_text, "foot")

        frame = MyFrame(urwid.AttrWrap(body, 'body'), header=header, footer=footer)
        frame.focus_position = 'header'
        return frame 
    def return_main(self, ignored=None):
        self.start(list.List)
def main():
    Detail().run()
if __name__=="__main__":
    main()
