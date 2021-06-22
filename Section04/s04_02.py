#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# s04_02.py（ButtonとそのEvent、さらに属性を追加したクラス）
#
import urwid
my_palette = [
    ('body', 'default', 'default'),
    ('foot', 'white', 'dark blue'),
    ('button', 'yellow', 'default'),
    ('button_focus', 'black', 'yellow'),
]

def create_mybutton(label, callback, user_data=None):
    button = urwid.Button(label, on_press=callback)
    return urwid.AttrMap(button, 'button', 'button_focus')

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
        self.txt.set_text(repr(k))

    def doformat(self):
        btn_t = create_mybutton("T", self.push_t)
        btn_s = create_mybutton("S", self.push_s)
        btn_q = create_mybutton("Q", self.exit)
        header = urwid.GridFlow([btn_t, btn_s, btn_q], 6, 1, 1, 'left')
        self.txt = urwid.Text(u"Buttonテスト")
        filler = urwid.Filler(self.txt, 'middle')
        self.foot_text = urwid.Text(u"これはフッター")
        footer = urwid.AttrWrap(self.foot_text, "foot")
        frame = urwid.Frame(urwid.AttrWrap(filler, 'body'), header=header, footer=footer)
        frame.focus_position = 'header'
        return frame 

    def run(self):
        self.main_loop = urwid.MainLoop(self.doformat(), my_palette, unhandled_input=self.unhandled_keypress)
        self.main_loop.run()

def main():
    Application().run()
if __name__=="__main__":
    main()
