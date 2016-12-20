#!/usr/bin/env python3
import sys
import os
import time
import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import * 
from threading import Thread
from wirm.wirm import WIRM
from storage.storage import db_api


class WebPage(QWebEnginePage):

    def __init__(self, status, hashed_key, process_name, window_title):
        super().__init__()
        self.status = status
        self.storage = db_api()
        self.hashed_key = hashed_key
        self.process_name = process_name
        self.window_title = window_title

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            # hashed_key = sys.argv[1]
            # process_name = sys.argv[2]
            # window_title = sys.argv[3]
            time = datetime.datetime.now().time()
            current_time = time.isoformat()
            text = msg
            if self.status == "new":
                self.storage.insert(self.hashed_key, text, current_time, self.window_title, self.process_name)
                self.status = "old"
                print("new note inserted")
            elif self.status == "old":
                self.storage.update(self.hashed_key, text, current_time, self.window_title, self.process_name)
                print("note updated")
        except OSError:
            pass


class NoteWindow(QWebEngineView):

    def __init__(self,x_position,y_position):
        super().__init__()
        file_path = '/ui/examples/richtext-simple.html'
        folder_path = os.path.abspath('./')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.abs_path = "file://" + folder_path + file_path
        self.setGeometry(x_position,y_position,250,280)
        self.setWindowTitle("LazyNotes")
        self.setWindowIcon(QIcon('graphics/notes.png'))
        self.load(QUrl(self.abs_path))
        self.setVisible(True)


class TrayIcon(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.wirm = WIRM()
        self.setIcon(QIcon('graphics/notes.png'))
        self.activated.connect(self.tray_icon_activated)
        self.create_menu()
        self.show()
        self.hashed_key = ""
        self.window_title = ""
        self.process_name = ""
        self.position = self.geometry().topRight()
        self.x_position = int(self.position.x())
        self.y_position = int(self.position.y())
        if self.x_position <= 0 :
            self.x_position = QCursor().pos().x()
            self.y_position = QCursor().pos().y()
        self.storage = db_api()
        self.note_window = NoteWindow(self.x_position,self.y_position)

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
        self.window_title = self.wirm.get_active_window_title()
        print("window_title: " + self.window_title)
        self.process_name = self.__make_cli_friendly(self.wirm.get_active_window_name())
        print("process_name: " + self.process_name)
        #storage = db_api()
        self.hashed_key = self.storage.get_hash(self.process_name, self.window_title)
        print("hashed_key "+self.hashed_key)
        #cmd = "python3 note_window.py " + str(hashed_key) + " " + str(process_name) + " " + str(window_title) \
        #      + " " + str(self.position.x()) + " " + str(self.position.y())
        #print(cmd)
        #os.system(cmd)
        note = self.storage.read_note_from_db(self.hashed_key)
        if note:
            default_text = note.note_attr_obj.note_info
            status = "old"
        else:
            default_text = "empty" 
            status = "new"

        #self.note_window = NoteWindow()
        page = WebPage(status, self.hashed_key, self.process_name, self.window_title)
        self.note_window.setPage(page)
        self.note_window.page().runJavaScript(str("window.onload = function() { init();firepad.setHtml('" + default_text + "')}"))
        self.note_window.load(QUrl(self.note_window.abs_path))
        self.note_window.setVisible(True)


    def tray_icon_activated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.show_note()


if __name__ == '__main__':
    app=QApplication(sys.argv) 
    app.setQuitOnLastWindowClosed(False)
    trayicon=TrayIcon()
    app.exec_()

