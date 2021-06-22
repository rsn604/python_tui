#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# s04_01.py（ButtonとそのEventを追加したクラス）
#
import urwid
class Application:
    main_loop = None

    def __init__(self):
        pass

    def push_t(self, button=None):
        self.foot_text.set_text("Pushed 'T'")

    def push_s(self, button=None):
        self.foot_text.set_text("Pushed 'S'")

    def exit(self, button=None):
        raise urwid.ExitMainLoop()

    def unhandled_keypress(self, k):
        if k in ('q', 'Q'):
            self.exit()
        self.text.set_text(repr(k))

    def doformat(self):
        btn_t  = urwid.Button("T", self.push_t)
        btn_s = urwid.Button("S", self.push_s)
        btn_q = urwid.Button("Q", self.exit)
        header = urwid.GridFlow([btn_t, btn_s, btn_q], 6, 1, 1, 'left')
        self.text = urwid.Text(u"Buttonテスト")
        filler = urwid.Filler(self.text, 'middle')
        self.foot_text = urwid.Text(u"これはフッター")
        frame = urwid.Frame(filler, header=header, footer=self.foot_text)
        frame.focus_position = 'header'
        return frame 

    def run(self):
        self.main_loop = urwid.MainLoop(self.doformat(), unhandled_input=self.unhandled_keypress)
        self.main_loop.run()

def main():
    Application().run()
if __name__=="__main__":
    main()
