#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urwid
import time

#---------------------------------------------------
# Pallete
#---------------------------------------------------
my_palette = [
    ('body', 'default', 'default'),
    ('foot', 'white', 'dark blue'),
    ('button', 'yellow', 'default'),
    ('button_focus', 'black', 'yellow'),
    ('search', 'yellow,underline', 'black'),
    ('edit', 'white', 'black'),
    ('edit_focus', 'yellow', 'black'),
    ('listwalker', 'black', 'light cyan'),
    ('label', 'light cyan,bold', 'default')
]

#---------------------------------------------------
# Standard button
#---------------------------------------------------
def create_mybutton(label, callback, user_data=None):
    return urwid.AttrMap(MyButton(label, on_press=callback, user_data=user_data), 'button', 'button_focus')
        
#---------------------------------------------------
# Standard edit
#---------------------------------------------------
def create_myedit(edit_text, align='left', multiline=False):
    return urwid.AttrMap(urwid.Edit(edit_text=edit_text, align=align, multiline=multiline), 'edit', 'edit_focus')

#---------------------------------------------------
# Standard label
#---------------------------------------------------
def create_mylabel(label):
    return urwid.AttrMap(urwid.Text(label, align="left"), "label")

#---------------------------------------------------
# Dialog
#---------------------------------------------------
def my_dialog(main_loop, overlay, align="center", valign="middle", width=30, height=15, min_width=0, min_height=0):
    main_loop.widget = urwid.Overlay(overlay, main_loop.widget, align=align, valign=valign, width=width, height=height)

#---------------------------------------------------
# Select box
#---------------------------------------------------
def my_select_box(main_loop, entries, current, title, callback):
    body = []
    selected = -1

    for i, entry in enumerate(entries):
        if entry == current:
            selected = i
        button = MyButton(entry, callback)
        body.append(urwid.AttrMap(button, None, 'button_focus'))

    listbox = urwid.ListBox(urwid.SimpleFocusListWalker(body))
    if selected >= 0:
        listbox.focus_position = selected
    my_dialog(main_loop, urwid.LineBox(listbox, title=title))

# -------------------------------------------
# Message box
# -------------------------------------------
def my_message_box(main_loop, title, callback):
    btn_OK = create_mybutton("OK", callback)
    btn_Cancel = create_mybutton("Cancel", callback)
    ok_cancel = urwid.GridFlow([btn_OK, btn_Cancel], 10, 1, 1, 'center')
    pile = [
        urwid.Divider(),
        urwid.Padding(ok_cancel)
    ]
    my_dialog(main_loop, urwid.LineBox(urwid.Filler(urwid.Pile(pile)), title=title, title_align='left'), height=7, align=('relative', 40), valign=('relative', 10))

#---------------------------------------------------
# Frame
#---------------------------------------------------
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

#---------------------------------------------------
# Button
#---------------------------------------------------
class MyButton(urwid.Button):
    def keypress(self, size, key):
        if key in ('h', 'H'):
            key = "left"
        elif key in ('j', 'J'):
            key = "down"
        elif key in ('k', 'K'):
            key =  "up"
        elif key in ('l', 'L'):
            key = "right"
        return super(MyButton, self).keypress(size, key)

#---------------------------------------------------
# Text
#---------------------------------------------------
class MyText(urwid.Text):
    def selectable(self):
        return True

    def keypress(self, size, key):
        if key in ('j', 'J'):
            return "down"
        elif key in ('k', 'K'):
            return "up"
        return key

#---------------------------------------------------
# Search edit
#---------------------------------------------------
class MySearchEdit(urwid.Edit):
    press_enter = None
    def keypress(self, size, key):
        if key == 'enter' and self.press_enter:
            self.press_enter(self.get_edit_text())
        elif key == 'esc' :
            self.edit_text = ""
        elif key == 'tab' :
            return "down"
        elif key == 'down' :
            return "down"
        #urwid.Edit.keypress(self, (size[0],), key)
        urwid.Edit.keypress(self, size, key) 
