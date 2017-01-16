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
from storage.storage import db_api
from functools import partial

note_visible_flag = 0
window_change_event_flag = 0
APP_NAME = "LazyNotes"




class WebPage(QWebEnginePage):

    def __init__(self, status, hashed_key, process_name, window_title):
        super().__init__()
        self.status = status
        self.storage = db_api()
        self.hashed_key = hashed_key
        self.process_name = process_name
        self.window_title = window_title

    def updatePage(self, status, hashed_key, process_name, window_title):
        self.status = status
        self.storage = db_api()
        self.hashed_key = hashed_key
        self.process_name = process_name
        self.window_title = window_title

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            time = datetime.datetime.now().time()
            current_time = time.isoformat()
            text = msg
            if self.status == "new":
                self.storage.insert(self.hashed_key, text, current_time, self.window_title, self.process_name)
                self.status = "old"
                print("new note inserted")
            elif self.status == "old":
                self.storage.update(self.hashed_key, text, current_time, self.window_title, self.process_name)
                print("window :"+self.process_name)
                print("window :"+self.hashed_key)
                print("note updated")
        except OSError:
            pass


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
        self.setVisible(True)
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
        self.wirm = WIRM()
        print("wirm")
        self.setIcon(QIcon('graphics/notes.png'))
        self.activated.connect(self.tray_icon_activated)
        self.create_menu()
        self.show()
        self.thread_scheduler = 0
        self.hashed_key = ""
        self.window_title = ""
        self.process_name = ""
        self.default_text = ""
        self.status = ""
        self.storage = db_api()
        self.get_note()
        self.note_window = NoteWindow()
        self.note_window.window_change_event_flag = 0
        self.page = WebPage(self.status, self.hashed_key, self.process_name, self.window_title)
        self.note_window.setPage(self.page)
        self.note_window.page().runJavaScript(str("window.onload = function() { init();firepad.setHtml('" + self.default_text + "')}"))
        self.note_window.load(QUrl(self.note_window.abs_path))
        self.note_window.setVisible(False)
        self.window_change_thread()


    def window_change_thread(self):
        global window_change_event_flag
        window_change_event_flag = 1
        t = threading.Thread(target=self.window_change_event)
        t.start()


    def window_change_event(self):
        global window_change_event_flag
        global note_visible_flag
        display = Xlib.display.Display(str(os.environ["DISPLAY"]))
        root = display.screen().root
        root.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
        print("__________in thread  "+str(self.note_window.window_change_event_flag))
        while (window_change_event_flag == 1):
            atom = display.intern_atom('_NET_ACTIVE_WINDOW',True)
            active_window_id = (root.get_full_property(atom, Xlib.X.AnyPropertyType).value[0])
            active = display.create_resource_object('window', active_window_id) 
            atom = display.intern_atom('_NET_WM_NAME',True)
            try:
                w = (active).get_full_property(atom, Xlib.X.AnyPropertyType).value
            except:
                continue
            if(w.decode("utf8") != self.win):
                self.win = w.decode("utf8")
                if(str(os.environ["DESKTOP_SESSION"]) == "xubuntu" or str(os.environ["DESKTOP_SESSION"]) == "xfce"):
                    while(self.wirm.thread_scheduler == self.thread_scheduler):
                        if(self.wirm.thread_scheduler == -1):   # Wirm Thread Stopped
                            return
                        continue
                self.thread_scheduler = not self.thread_scheduler
                print ('!!!Window changed!!!!')
                self.show_note()
            time.sleep(0.1)
        print("main_app thread stopped!!")

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

    def get_note(self, session_num = 1):
        global APP_NAME
        while(self.wirm.active_window_thread_flag == 0):
            continue
        self.window_title = str(self.wirm.get_active_window_title(session_num))
        if(self.window_title == APP_NAME):
            print(APP_NAME)
            return False
        print(self.window_title)
        self.process_name = self.wirm.get_active_window_name(session_num)
        print("window_title: " + str(self.window_title))
        print("process_name: " + self.process_name)
        self.hashed_key = self.storage.get_hash(self.process_name, self.window_title)
        print("hashed_key "+self.hashed_key)
        note = self.storage.read_note_from_db(self.hashed_key)
        if note:
            self.default_text = note.note_attr_obj.note_info
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

