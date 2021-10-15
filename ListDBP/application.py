#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urwid
from mywidget import my_palette

class Application:
    main_loop = None
    cols = None
    rows = None

    #---------------------------------------------------
    # Set 'Singleton'
    #---------------------------------------------------
    @classmethod
    def get_instance(cls, common=None):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(common)
        else:
            cls._instance.common = common
        return cls._instance

    #---------------------------------------------------
    # Exit
    #---------------------------------------------------
    def exit(self, button=None):
        raise urwid.ExitMainLoop()

    #---------------------------------------------------
    # get terminal size
    #---------------------------------------------------
    def get_cols_rows(self):
        try :
            cols, rows = urwid.raw_display.Screen().get_cols_rows()
            return cols, rows-2
        except OSError:
            if self.cols != None and self.rows != None:
                return self.cols, self.rows
            else:
                return None, None

    #---------------------------------------------------
    # Unhandled keypress : override this method. 
    #---------------------------------------------------
    def unhandled_keypress(self, k):
        return True
    
    #---------------------------------------------------
    # Format screen : override this method. 
    #---------------------------------------------------
    def doformat(self):
        return urwid.widget

    #---------------------------------------------------
    # Diaplay : draw_screen.  
    #---------------------------------------------------
    def display(self):
        self.main_loop.widget = self.doformat()

    #---------------------------------------------------
    # Start
    #---------------------------------------------------
    def start(self, next_class, common=None):
        next_class.get_instance(common).run(self.main_loop, self.cols, self.rows)

    #---------------------------------------------------
    # Initiate application.
    #---------------------------------------------------
    def run(self, main_loop=None, cols=None, rows=None):
        urwid.set_encoding('UTF-8')

        # --------------------------------------------------
        # Open raw_display.Screen() and main_loop only once .
        # --------------------------------------------------
        if cols == None:
            self.cols, self.rows = self.get_cols_rows()
        else:
            self.cols = cols
            self.rows = rows
        
        # --------------------------------------------------
        # Setting main_loop
        # --------------------------------------------------
        if main_loop != None:
            self.main_loop = main_loop
            self.main_loop.unhandled_input = self.unhandled_keypress
            self.display()
        else:
            self.main_loop = urwid.MainLoop(self.doformat(), my_palette, unhandled_input=self.unhandled_keypress)
            self.main_loop.run()
