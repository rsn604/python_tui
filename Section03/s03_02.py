#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# s03_02.py
#
import urwid

class Application:
    main_loop = None
    def __init__(self):
        pass
    
    def exit(self):
        raise urwid.ExitMainLoop()

    def unhandled_keypress(self, k):
        if k in ('q', 'Q'):
            self.exit()
        self.text.set_text(repr(k))
    
    def doformat(self):
        self.text = urwid.Text(u"Hello World")
        filler = urwid.Filler(self.text, 'middle')
        frame = urwid.Frame(filler)
        return frame 

    def run(self):
        self.main_loop = urwid.MainLoop(self.doformat(), unhandled_input=self.unhandled_keypress)
        self.main_loop.run()

def main():
    Application().run()

if __name__=="__main__":
    main()
