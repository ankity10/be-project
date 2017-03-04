#!/usr/bin/env python3
import threading
import Xlib.display
import Xlib.threaded
import sys
import os
import time
import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import * 
from wirm.wirm import WIRM
from storage.storage2 import Db
from storage.storage2 import Note
import hashlib
from functools import partial

note_visible_flag = 0
window_change_event_flag = 0
APP_NAME = "LazyNotes"




class WebPage(QWebEnginePage):

    def __init__(self, status, hashed_key, process_name, window_title):
        super().__init__()
        self.status = status
        self.storage = Db()
        self.hashed_key = hashed_key
        self.process_name = process_name
        self.window_title = window_title

    def updatePage(self, status, hashed_key, process_name, window_title):
        self.status = status
        self.storage = Db()
        self.hashed_key = hashed_key
        self.process_name = process_name
        self.window_title = window_title

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            print("error message is: ",msg, " at linenumber ", linenumber)
            delimeter = ":"
            delimeter_index = 9
            index = msg.index(delimeter)
            if index == delimeter_index:
                msg_list = msg.split(delimeter)[1]
                self.save_note(str(msg_list))
        except ValueError:
            pass # relace this with proper error handeling
            # Error raised by javascript
            # msg: error message


    def save_note(self, msg):
        try:
            note_dict = {"create_time": datetime.datetime.now().time().isoformat(), "text": msg, "process_name": self.process_name, "window_title": self.window_title}
            note = Note(**note_dict)
            if self.status == "new":
                self.storage.insert_note(note)
                self.status = "old"
                print("new note inserted")
            elif self.status == "old":
                self.storage.update_note(note)
        except OSError:
            pass # replace this with error handeling
            # system related error


class NoteWindow(QWebEngineView):

    def __init__(self):
        global window_change_event_flag
        super().__init__()
        file_path = '/ui/examples/richtext-simple.html'
        folder_path = os.path.abspath('./')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.abs_path = "file://" + folder_path + file_path
        self.setWindowTitle("LazyNotes")
        self.setWindowIcon(QIcon('graphics/notes.png'))
        self.load(QUrl(self.abs_path))
        self.setVisible(False)
        window_change_event_flag = 0

    def closeEvent(self,event):
        global note_visible_flag
        self.setVisible(False) 
        note_visible_flag = 0
        event.ignore()      


class TrayIcon(QSystemTrayIcon):

    def __init__(self):
        self.win = ""
        super().__init__()
        print("wirm")
        self.setIcon(QIcon('graphics/notes.png'))
        self.activated.connect(self.tray_icon_activated)
        self.create_menu()
        self.show()
        self.x_position = 0
        self.y_position = 0
        self.thread_scheduler = 0
        self.hashed_key = ""
        self.window_title = ""
        self.process_name = ""
        self.default_text = ""
        self.status = ""
        self.storage = Db()
        #self.get_note()
        self.note_window = NoteWindow()
        #self.note_window.window_change_event_flag = 0
        self.page = WebPage(self.status, self.hashed_key, self.process_name, self.window_title)
        self.note_window.setPage(self.page)
        # self.note_window.page().runJavaScript(str())
        self.note_window.load(QUrl(self.note_window.abs_path))
        print("--------------------------------------------------------------------")
        self.wirm = WIRM(self)
        self.note_window.setVisible(False)
        #self.window_change_thread()

    def create_menu(self):
        self.tray_icon_menu = QMenu()
        shownote = QAction('Note',self)
        shownote.triggered.connect(partial(self.show_note_menu,0))
        self.tray_icon_menu.addAction(shownote)
        self.tray_icon_menu.addSeparator()
        exitaction = QAction('Exit',self)
        exitaction.triggered.connect(self.exit_app)
        self.tray_icon_menu.addAction(exitaction)
        self.setContextMenu(self.tray_icon_menu)

    def show_note_menu(self,session_num = 1):   # To separate thread function from show_note function
        global note_visible_flag
        # self.note_window.page().runJavaScript(str("init();"))

        self.show_note(session_num)
        if self.x_position == 0:
            position = self.geometry().topRight()
            self.x_position = int(position.x())
            self.y_position = int(position.y())
            if self.x_position <= 0 :
                self.x_position = QCursor().pos().x()
                self.y_position = QCursor().pos().y()
            self.note_window.setGeometry(self.x_position,self.y_position,250,280)
        self.note_window.setVisible(True)
        note_visible_flag = 1


    def show_note(self,session_num = 1):    #sesion_num = 0 when note option is clicked(for xfce), else 1
        global note_visible_flag
        if(self.get_note(session_num) == False):
            return
        self.page.updatePage(self.status, self.hashed_key, self.process_name, self.window_title)
        self.note_window.page().runJavaScript(str("firepad.setHtml('"+self.default_text+"')"))
        #self.page.updatePage(self.status, self.hashed_key, self.process_name, self.window_title)
        

    def exit_app(self):
        global window_change_event_flag
        window_change_event_flag = 0
        self.wirm.active_window_thread_flag = 0
        sys.exit(0)

    def calc_hash(self, **kwargs):
        sha256 = hashlib.sha256()
        sha256.update((kwargs['process_name'] + kwargs['window_title']).encode('utf-8'))
        hash_value = sha256.hexdigest()
        return hash_value

    def get_note(self, session_num = 1):
        global APP_NAME
        while(self.wirm.active_window_thread_flag == 0):
            continue
        self.window_title = str(self.wirm.get_active_window_title(session_num))
        if(self.window_title == APP_NAME):
            print(APP_NAME)
            return False
        #print(self.window_title)
        self.process_name = self.wirm.get_active_window_name(session_num)
        self.hashed_key = self.calc_hash(process_name = self.process_name,window_title = self.window_title)
        #print("hashed_key "+self.hashed_key)
        note = self.storage.read_note(self.hashed_key)
        if note:
            #self.default_text = note.note_attr_obj.note_info
            self.default_text = note.text
            self.status = "old"
        else:
            self.default_text = "empty" 
            self.status = "new"
        return True

    def tray_icon_activated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.get_note()


if __name__ == '__main__':
    app=QApplication(sys.argv) 
    app.setQuitOnLastWindowClosed(False)
    trayicon=TrayIcon()
    app.exec_()

