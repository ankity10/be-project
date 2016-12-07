#!/usr/bin/env python3
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import * 
import time
from threading import Thread
from wirm.wirm import WIRM
from data_filter.data_filter import DataFilter

class TrayIcon(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.wirm = WIRM()
        self.setIcon(QIcon('graphics/notes.png'))
        self.activated.connect(self.tray_icon_activated)
        self.create_menu()
        self.show()

    def __make_cli_friendly(self, string):
        return string.translate(str.maketrans({"-":  r"\-",
                                                                            "]":  r"\]",
                                                                            "\\": r"\\",
                                                                            "^":  r"\^",
                                                                            "$":  r"\$",
                                                                            "*":  r"\*",
                                                                            ".":  r"\.",
                                                                            "(":  r"-",
                                                                            ")":  r"_",
                                                                            " ":  r"\ "}))


    def create_menu(self):
        self.tray_icon_menu = QMenu()
        shownote = QAction('Note',self)
        shownote.triggered.connect(self.show_note)
        self.tray_icon_menu.addAction(shownote)
        self.tray_icon_menu.addSeparator()
        exitaction = QAction('Exit',self)
        exitaction.triggered.connect(self.exit_app)
        self.tray_icon_menu.addAction(exitaction)
        self.setContextMenu(self.tray_icon_menu)

    def exit_app(self):
        self.wirm.active_window_thread_flag = 0
        sys.exit(0)

    def show_note(self):
        self.position = self.geometry().topRight()
        window_title = self.__make_cli_friendly(self.wirm.get_active_window_title())
        print("window_title: " + window_title)
        process_name = self.__make_cli_friendly(self.wirm.get_active_window_name())
        print("process_name: " + process_name)
        d = DataFilter()
        hashed_key = self.__make_cli_friendly(d.get_hash(process_name, window_title))
        print("hashed_key "+hashed_key)

        cmd = "python3 note_window.py " + str(hashed_key) + " " + str(process_name) + " " + str(window_title) \
              + " " + str(self.position.x()) + " " + str(self.position.y())
        print(cmd)
        os.system(cmd)

    def tray_icon_activated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.show_note()


if __name__ == '__main__':
    app=QApplication(sys.argv) 
    app.setQuitOnLastWindowClosed(False)
    trayicon=TrayIcon()
    app.exec_()

