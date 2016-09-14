#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

import sys
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QSystemTrayIcon, QApplication, QMenu, QAction, QWidget, QTextEdit,QVBoxLayout, QPushButton)


# GLOBALS

global nwindow_status 
nwindow_status = 'closed'


class MainWindow(QObject):
    
    def __init__(self):
        super().__init__()    
        self.init_UI()
    
    def init_UI(self):
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
        print("asasd")
        sys.exit(0)


class StatusIcon:
    def __init__(self):
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.set_from_stock(Gtk.STOCK_HOME)
        self.status_icon.connect("activate", self.activate)
        self.nwindow_status = 'closed'

    def activate(self, widget):
        if self.nwindow_status == 'closed':
            print("window was closed")
            self.start_nwindow()
        elif self.nwindow_status == 'open':
            print("window was opened")
            self.close_nwindow()
            

    def start_nwindow(self):
        self.nwindow_status = 'open'
        print(self.nwindow_status)
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.app.exec_()
        

    def close_nwindow(self):
        self.app.closeAllWindows()
        self.nwindow_status = 'closed'

app = StatusIcon()
Gtk.main()