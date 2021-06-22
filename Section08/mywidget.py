#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mywidget.py
#
import urwid
import time

def get_items(name):
    items = []
    for i in range(100):
        item = []
        item.append(name+str(i))
        item.append(name+str(i)+" フィールド02")
        item.append("改行を含む入力データ\n2行目のデータ\n3行目のデータ")
        items.append(item)
    return items

my_palette = [
    ('body', 'default', 'default'),
    ('foot', 'white', 'dark blue'),
    ('button', 'yellow', 'default'),
    ('button_focus', 'black', 'yellow'),
    ('edit', 'white', 'black'),
    ('edit_focus', 'yellow', 'black'),
    ('listwalker', 'black', 'light cyan'),
    ('label', 'light cyan,bold', 'default')
]

def create_mybutton(label, callback, user_data=None):
    button = urwid.Button(label, on_press=callback)
    return urwid.AttrMap(button, 'button', 'button_focus')

def create_myedit(edit_text, align='left', multiline=False):
    return urwid.AttrMap(urwid.Edit(edit_text=edit_text, align=align, multiline=multiline), 'edit', 'edit_focus')

def create_mylabel(label):
    return urwid.AttrMap(urwid.Text(label, align="left"), "label")

class MyText(urwid.Text):
    def selectable(self):
        return True
    def keypress(self, size, key):
        if key in ('j', 'J'):
            return "down"
        elif key in ('k', 'K'):
            return "up"
        return key

class MyFrame(urwid.Frame):
    last_time_clicked = None
    double_click = None
    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press':
            now = time.time()
            if (self.last_time_clicked and (now - self.last_time_clicked < 0.5)):
                if self.double_click:
                    self.double_click()
            else:
                urwid.Frame.mouse_event(self, size, event, button, col, row, focus)                
            self.last_time_clicked = now

