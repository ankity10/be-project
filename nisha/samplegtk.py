#!/usr/bin/env python
import os
from gi.repository import Gtk
from gi.repository import AppIndicator3

class AppIndicatorExample:
    def __init__(self, indicator_id):
        self.ind = AppIndicator3.Indicator.new(str(indicator_id), os.path.abspath('icon.png'), AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        # create a menu
        self.menu = Gtk.Menu()

        item_note = Gtk.MenuItem('Note')
        item_note.connect("activate",self.show_note)
        item_note.show()
        self.menu.append(item_note)

        item_exit = Gtk.MenuItem('Quit')
        item_exit.connect("activate", self.quit)
        item_exit.show()
        self.menu.append(item_exit)

        self.menu.show()

        self.ind.set_menu(self.menu)

    def quit(self,data=None):
        Gtk.main_quit()

    def show_note(self,data=None):
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


if __name__ == "__main__":
    indicator = AppIndicatorExample(1)

    Gtk.main()