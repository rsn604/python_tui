#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# application.py
#
import urwid
from mywidget import my_palette

class Application:
    main_loop = None
    def exit(self, button=None):
        raise urwid.ExitMainLoop()
    def get_cols_rows(self):
        cols, rows = urwid.raw_display.Screen().get_cols_rows()
        return cols, rows-2
    def unhandled_keypress(self, k):
        return True
    def doformat(self):
        return urwid.widget
    def display(self):
        self.main_loop.widget = self.doformat()
    def start(self, next_class):
        next_class().run(self.main_loop)
    def run(self, main_loop=None):
        if main_loop != None:
            self.main_loop = main_loop
            self.main_loop.unhandled_input = self.unhandled_keypress
            self.display()
        else:
            self.main_loop = urwid.MainLoop(self.doformat(), my_palette, unhandled_input=self.unhandled_keypress)
            self.main_loop.run()
