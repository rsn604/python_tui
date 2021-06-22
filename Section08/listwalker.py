#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# listwalker.py
#
import urwid
from mywidget import MyText

class ListWalker(urwid.ListWalker):
    def __init__(self, items, from_rec, rows):
        self.focus = 0
        self.create_page(items, from_rec, rows)
    
    def create_page(self,items, from_rec, rows):
        self.lines = []
        self.is_last = False
        for i in range(rows):
            if len(items) < from_rec + i:
                self.is_last = True
                break
            #text = MyText(items[from_rec+i-1])
            text = MyText(items[from_rec+i-1][0])
            self.lines.append(urwid.AttrMap(text, None, 'listwalker'))

    def last_page(self):
        return self.is_last
        
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

