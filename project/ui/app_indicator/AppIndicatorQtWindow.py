import sys
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QSystemTrayIcon, QApplication, QMenu, QAction, QWidget, QTextEdit,QVBoxLayout, QPushButton)

import threading
from queue import Queue
import time


class Example(QObject):
    
    def __init__(self):
        super().__init__()    
        self.initUI()
    
    def initUI(self):
        self.w = QWidget()
        # self.w.setWindowTitle("Ankit")
        self.layout = QVBoxLayout()
        self.edit = QTextEdit()
        txt = open('note.txt')
        self.edit.append(txt.read())
        # self.edit.append(str(reason))
        txt.close()
        self.button = QPushButton('Save')
        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.save_note)
        self.w.setLayout(self.layout)
        self.w.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.w.show()
            
    def save_note(self):
        mytext = self.edit.toPlainText()
        with open('note.txt','w') as txt:
            txt.write(mytext)

    def closeEvent(self, event):
        sys.exit(0)


def start_note_window():    
    app = QApplication(sys.argv)
    ex = Example()
    app.exec_()


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
        self.ind.set_secondary_activate_target(item_note)

    def quit(self,data=None):
        Gtk.main_quit()

    def show_note(self,data=None):
        start_note_window()
        

        # t = threading.Thread(target=start_note_window)
        # # t.daemon = True
        # t.start


if __name__ == "__main__":
    indicator = AppIndicatorExample(1)

    Gtk.main()
