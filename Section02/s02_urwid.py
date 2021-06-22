#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# s02_urwid.py
#
import urwid
class MyEdit(urwid.Edit):
    def keypress(self, size, key):
        if key != 'enter':
            return super(MyEdit, self).keypress(size, key)
        else:
            raise urwid.ExitMainLoop()

edit = MyEdit(u"お名前は? ")
loop = urwid.MainLoop(urwid.Filler(edit))
loop.run()
