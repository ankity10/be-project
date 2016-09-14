#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QSystemTrayIcon, QApplication, QMenu, QAction, QWidget, QTextEdit,QVBoxLayout, QPushButton)


class MyStatusIconApp:
    def __init__(self):
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.set_from_stock(Gtk.STOCK_HOME)
        self.status_icon.connect("popup-menu", self.right_click_event)
        self.status_icon.connect("activate", self.show_about_dialog)

    def right_click_event(self, icon, button, time):
        self.menu = Gtk.Menu()

        about = Gtk.MenuItem()
        about.set_label("About")
        about.connect("activate", self.show_about_dialog)
        self.menu.append(about)

        quit = Gtk.MenuItem()
        quit.set_label("Quit")
        quit.connect("activate", Gtk.main_quit)
        self.menu.append(quit)

        self.menu.show_all()

        self.menu.popup(None, None, None, self.status_icon, button, time)


    def show_about_dialog(self, widget):
        self.window = Gtk.Window()
        self.layout = Gtk.Layout()
        self.box = Gtk.Box()
        self.window.set_title("Note")
        self.buffer1 = Gtk.TextBuffer()
        self.Textbox = Gtk.TextView(buffer=self.buffer1)
        #self.buffer1 = self.Textbox.get_buffer()
        with open("note.txt", 'r') as f:
            data = f.read()
            self.buffer1.set_text(data)
        self.box.add(self.Textbox)
        self.window.add(self.box)
        self.window.show_all()

app = MyStatusIconApp()
Gtk.main()