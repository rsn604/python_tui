#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# s05_03.py（ListBox内に表示できるText件数を考慮する）
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

class MyText(urwid.Text):
    def selectable(self):
        return True

    def keypress(self, size, key):
        if key in ('j', 'J'):
            return "down"
        elif key in ('k', 'K'):
            return "up"
        return key

class ListWalker(urwid.ListWalker):
    def __init__(self, items, rows):
        self.focus = 0
        self.create_page(items, rows)
    
    def create_page(self,items, rows):
        self.lines = []
        self.is_last = False
        for i in range(rows):
            text = MyText(items[i])
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

    def get_cols_rows(self):
        cols, rows = urwid.raw_display.Screen().get_cols_rows()
        return cols, rows-2

    def select_list(self):
        focus_widget, idx = self.listbox.get_focus()
        self.footer_text.set_text("pos:"+str(idx)+" data:"+focus_widget.base_widget.text)

    def unhandled_keypress(self, k):
        if self.main_loop.widget.focus_position == 'header' and k == 'down':
            self.main_loop.widget.focus_position = 'body'
        elif self.main_loop.widget.focus_position == 'body' and k == 'up':
            self.main_loop.widget.focus_position = 'header'

        if k in ('q', 'Q'):
            self.exit()        
        elif k == 'enter':
            self.select_list()
        else:
            return
    
    def doformat(self):
        cols, rows = self.get_cols_rows()
        walker = ListWalker(get_items(), rows)
        self.listbox = urwid.ListBox(walker)

        btn_q = create_mybutton("Q", self.exit)
        header = urwid.GridFlow([btn_q], 6, 1, 1, 'left')

        self.footer_text = urwid.Text(u"これはフッター")
        footer = urwid.AttrWrap(self.footer_text, "foot")

        frame = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'), header=header, footer=footer)
        frame.focus_position = 'header'
        return frame 

    def run(self):
        urwid.set_encoding('UTF-8')
        self.main_loop = urwid.MainLoop(self.doformat(), my_palette, unhandled_input=self.unhandled_keypress)
        self.main_loop.run()

def main():
    Application().run()

if __name__=="__main__":
    main()
