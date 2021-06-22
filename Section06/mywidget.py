#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mywidget.py
#
import urwid
import time

def get_items():
    items = []
    for i in range(100):
        items.append("テストデータ"+str(i))
    return items

my_palette = [
    ('body', 'default', 'default'),
    ('foot', 'white', 'dark blue'),
    ('button', 'yellow', 'default'),
    ('button_focus', 'black', 'yellow'),
    ('listwalker', 'black', 'light cyan')
]

def create_mybutton(label, callback, user_data=None):
    button = urwid.Button(label, on_press=callback)
    return urwid.AttrMap(button, 'button', 'button_focus')

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

