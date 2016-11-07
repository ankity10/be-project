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
        self.setIcon(QIcon('graphics/notes.png'))
        self.activated.connect(self.tray_icon_activated)
        self.create_menu()
        self.show()

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
        sys.exit(0)

    def show_note(self):
        # position = self.geometry().topRight()
        # print(wirm)
        w = WIRM()
        window_title = w.get_active_window_title().translate(str.maketrans({"-":  r"\-",
                                                                            "]":  r"\]",
                                                                            "\\": r"\\",
                                                                            "^":  r"\^",
                                                                            "$":  r"\$",
                                                                            "*":  r"\*",
                                                                            ".":  r"\.",
                                                                            "(":  r"-",
                                                                            ")":  r"_"}))

        print("window_title: " + window_title)
        process_name = w.get_active_window_name().translate(str.maketrans({"-":  r"\-",
                                                                            "]":  r"\]",
                                                                            "\\": r"\\",
                                                                            "^":  r"\^",
                                                                            "$":  r"\$",
                                                                            "*":  r"\*",
                                                                            ".":  r"\.",
                                                                            "(":  r"-",
                                                                            ")":  r"_"}))
        print("process_name: " + process_name)

        d = DataFilter()
        hashed_key = d.get_hash(process_name, window_title).translate(str.maketrans({"-":  r"\-",
                                                                                    "]":  r"\]",
                                                                                    "\\": r"\\",
                                                                                    "^":  r"\^",
                                                                                    "$":  r"\$",
                                                                                    "*":  r"\*",
                                                                                    ".":  r"\.",
                                                                                    "(":  r"-",
                                                                                    ")":  r"_"}))
        print("hashed_key "+hashed_key)
        cmd = "python3 note_window.py " + str(hashed_key) + " " + str(process_name) + " " + str(window_title)
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

