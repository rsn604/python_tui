#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# s02_npyscreen.py
#
import npyscreen
class TestApp(npyscreen.NPSApp):
    def main(self):
        F  = npyscreen.Form(name = "Welcome to Npyscreen",)
        t  = F.add(npyscreen.TitleText, name = "お名前は?",)
        F.edit()

if __name__ == "__main__":
    App = TestApp()
    App.run()
