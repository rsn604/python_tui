#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# s05_01.py（ListBoxを使ってみる）
#
import urwid

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

class ListWalker(urwid.ListWalker):
    def __init__(self, items):
        self.focus = 0
        self.create_page(items)
    
    def create_page(self,items):
        self.lines = []
        for item in items:
            text = urwid.Text(item)
            self.lines.append(urwid.AttrMap(text, None, 'listwalker'))
        
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

class Application:
    main_loop = None
    def __init__(self):
        pass

    def exit(self, button=None):
        raise urwid.ExitMainLoop()

    def unhandled_keypress(self, k):
        '''
        if self.main_loop.widget.focus_position == 'header' and k == 'down':
            self.main_loop.widget.focus_position = 'body'
        elif self.main_loop.widget.focus_position == 'body' and k == 'up':
            self.main_loop.widget.focus_position = 'header'
        '''
        if k in ('q', 'Q'):
            self.exit()        
        else:
            return
        return True
    
    def doformat(self, from_rec=1):
        walker = ListWalker(get_items())
        self.listbox = urwid.ListBox(walker)

        btn_q = create_mybutton("Q", self.exit)
        header = urwid.GridFlow([btn_q], 6, 1, 1, 'left')

        self.footer_text = urwid.Text(u"これはフッター")
        footer = urwid.AttrWrap(self.footer_text, "foot")

        frame = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'), header=header, footer=footer)
        frame.focus_position = 'header'
        return frame 

    def run(self):
        self.main_loop = urwid.MainLoop(self.doformat(), my_palette, unhandled_input=self.unhandled_keypress)
        self.main_loop.run()

def main():
    Application().run()

if __name__=="__main__":
    main()
