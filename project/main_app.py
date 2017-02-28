#!/usr/bin/env python3
import threading
import Xlib.display
import Xlib.threaded
import sys
import os
import time
import datetime
import hashlib
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import * 
from wirm.wirm import WIRM
from storage.storage2 import Db
from storage.storage2 import Note
from storage.storage2 import Local_Log
from storage.storage2 import Login_Credentials
from storage.storage2 import Saved_Password
from urllib.request import urlopen
from functools import partial

note_visible_flag = 0
window_change_event_flag = 0
APP_NAME = "LazyNotes"




class WebPage(QWebEnginePage):

    def __init__(self,main_app, status, hashed_key, process_name, window_title):
        super().__init__()
        self.main_app = main_app
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
            note_dict = {"create_time": datetime.datetime.now().time().isoformat(), "text": {str(self.main_app.client_id) : msg}, "process_name": self.process_name, "window_title": self.window_title, "hash_value":self.hashed_key}
            note = Note(**note_dict)
            local_log_dict = {}
            #############################################
            if(self.main_app.internet_on_flag != 1 or self.main_app.login_credentials.token == 0):
                local_log_dict = {"hash_value" :self.hashed_key,"text" :msg,"conflict_flag":False}
            else:
                local_log_dict = {"hash_value" :self.hashed_key,"text" :msg,"conflict_flag":True}
            local_log = Local_Log(**local_log_dict)
            if(self.storage.read_log(self.hashed_key) == None):
                self.storage.insert_log(local_log)
            else:
                self.storage.update_log(local_log)
            #############################################    
            if self.status == "new":
                self.storage.insert_note(note)
                self.status = "old"
                print("new note inserted")
            elif self.status == "old":
                if(self.main_app.internet_on_flag != 1 or self.main_app.login_credentials.token == 0):
                    old_note = self.storage.read_note(self.hashed_key)
                    note_dict["text"] = old_note.text
                    note_dict["text"][str(self.main_app.client_id)] = msg
                note = Note(**note_dict)
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
        self.setVisible(True)
        window_change_event_flag = 0

    def closeEvent(self,event):
        global note_visible_flag
        self.setVisible(False) 
        note_visible_flag = 0
        event.ignore()      

class LoginWindow(QWidget):
    def __init__(self,main_app,visible_flag = True):
        super().__init__()
        self.main_app = main_app
        self.visible_flag = visible_flag
        self.setMinimumSize(400, 400)
        self.setWindowTitle('Login/Sign Up')
        self.username_lbl = QLabel("Username :", self)
        self.username_lbl.move(5, 5) 
        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Username')
        self.username.setMinimumWidth(285)
        self.username.move(110, 5)
        self.password_lbl = QLabel("Password :", self)
        self.password_lbl.move(5, 30) 
        self.password = QLineEdit(self)
        self.password.setEchoMode(2)
        self.password.setPlaceholderText('Password')
        self.password.setMinimumWidth(285)
        self.password.move(110, 30)
        self.login_button = QPushButton("Log In",self)
        self.login_button.move(120,60)
        self.login_button.clicked.connect(self.login_method)
        self.setVisible(True)

    def login_method(self,username = "",password = ""):
        if(username == ""):
            self.username_text = self.username.text()
            self.password_text = self.password.text()
        else:
            self.username_text = username
            self.password_text = password
        login_response=urlopen(self.main_app.login_url,timeout=5)
        self.authentication_flag = login_response["authentication_flag"] 
        if(self.authentication_flag == False):
            auth_fail_msg = QMessageBox()
            auth_fail_msg.setIcon(QMessageBox.Information)
            auth_fail_msg.setText("Wrong User Name or Password!!")
            auth_fail_msg.setStandardButtons(QMessageBox.Ok)
            auth_fail_msg.show()
            auth_fail_msg.buttonClicked.connect(self.auth_fail_msg_btn)
            self.main_app.login.setVisible(True)
            self.main_app.logout.setVisible(False)
        else:
            self.token = login_response["token"]
            self.client_flag = login_response["client_flag"]
            self.main_app.storage.update_login_token(self.token)
            self.main_app.storage.insert_saved_password(self.username_text, self.password_text)
            if(self.client_flag == 0):   #New Client
                notes_dict = urlopen(self.main_app.notes_retrieve_url,timeout=5)
            self.main_app.sync = sync(self.main_app)
            self.main_app.login.setVisible(False)
            self.main_app.logout.setVisible(True)

    def auth_fail_msg_btn(self):
        self.show()

class ConflictResolveWidget(QWidget):
    def __init(self,main_app,note, window_title, hashed_key, process_name):
        super().__init__()
        self.window_title = window_title
        self.hashed_key = hashed_key
        self.process_name = process_name
        self.merged_text = ""
        self.note = note_window
        self.main_app = main_app
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        for client,text in self.note.items():
            self.client_lbl = QLabel("Client Id :"+str(client), self)
            view = QWebEngineView()
            view.setHtml(text)
            button = QPushButton("Keep Note!!")
            button.clicked.connect(partial(self.resolve_conflict,text))

    def resolve_conflict(self,text):
        local_log_dict = {"hash_value" :self.hashed_key,"text" :msg,"conflict_flag":True}
        local_log = Local_Log(**local_log_dict)
        if(self.storage.read_log(self.hashed_key) == None):
            self.storage.insert_log(local_log)
        else:
            self.storage.update_log(local_log)
        note_dict = {"create_time": datetime.datetime.now().time().isoformat(), "text": {self.main_app.client_id : text}, "process_name": self.process_name, "window_title": self.window_title, "hash_value":self.hashed_key}
        note = Note(**note_dict)
        self.storage.update_note(note)


class ConflictMsgBox(QMessageBox):
    def __init__(self, main_app, note, window_title, hashed_key, process_name):
        super().__init__()
        self.window_title = window_title
        self.hashed_key = hashed_key
        self.process_name = process_name
        self.option_flag = 0     # = 0, if box closed without selecting any option, else 1
        self.note = note    #Conflicting Notes
        self.main_app = main_app
        self.setIcon(QMessageBox.Information)
        self.setText("There is a Merge Conflict for this note!")
        self.setInformativeText("Do you want to resolve the merge conflict?")
        self.setWindowTitle("Merge Conflict")
        self.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        self.buttonClicked.connect(self.msg_btn)
        self.show()

    def msg_btn(self,btn):
        if(btn == "&Yes"):
            self.option_flag = 1
            if(self.main_app.internet_on_flag != 1):
                net_off_msg = QMessageBox()
                net_off_msg.setIcon(QMessageBox.Information)
                net_off_msg.setText("You are offline!")
                net_off_msg.setStandardButtons(QMessageBox.Ok)
                net_off_msg.show()
            elif(self.main_app.login_credentials.token == 0):
                logged_out_msg = QMessageBox()
                logged_out_msg.setIcon(QMessageBox.Information)
                logged_out_msg.setText("You are not Logged In!")
                logged_out_msg.setStandardButtons(QMessageBox.Ok)
                logged_out_msg.show()
            else:
                self.conflict_resolve_widget = ConflictResolveWidget(self.main_app,self.note,self.window_title,
                                                                     self.hashed_key, self.process_name)


class TrayIcon(QSystemTrayIcon):

    def __init__(self):
        self.notes_retrieve_url = ""
        self.login_url = ""
        self.internet_on_flag = -1
        self.win = ""
        super().__init__()
        print("wirm")
        self.internet_check_thread_flag = 1
        self.storage = Db()
        self.login_credentials = self.storage.read_login_credentials()
        self.client_id = self.login_credentials.client_id
        t = threading.Thread(target=self.internet_check_thread)
        t.start()
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
        #self.get_note()
        self.note_window = NoteWindow()
        #self.note_window.window_change_event_flag = 0
        self.init_login()   # Login attempt from stored username & password
        self.page = WebPage(self,self.status, self.hashed_key, self.process_name, self.window_title)
        self.note_window.setPage(self.page)
        self.note_window.page().runJavaScript(str("window.onload = function() { init();firepad.setHtml('"+self.default_text+"');}"))
        self.note_window.load(QUrl(self.note_window.abs_path))
        print("--------------------------------------------------------------------")
        self.wirm = WIRM(self)
        self.note_window.setVisible(False)
        #self.window_change_thread()


    def init_login(self):
        while(self.internet_on_flag == -1):
            continue
        if(self.internet_on_flag == 0):
            self.logout.setVisible(True)
        else:
            saved_password = self.storage.read_saved_password()
            if(saved_password == None):
                self.logout.setVisible(True)
            else:
                login_window = LoginWindow(self,False)
                login_window.login_method(saved_password.username,saved_password.password)


    def internet_check_thread(self):
        while(self.internet_check_thread_flag == 1):
            if(self.internet_on() == True):
                self.internet_on_flag = 1
            else:
                self.internet_on_flag = 0


    def internet_on(self):
        for timeout in [1,5,10,15]:
            try:
                response=urlopen('http://google.com',timeout=timeout)
                return True
            except urllib.error.URLError as err: pass
        return False

    def create_menu(self):
        self.tray_icon_menu = QMenu()
        shownote = QAction('Note',self)
        shownote.triggered.connect(partial(self.show_note_menu,0))
        self.tray_icon_menu.addAction(shownote)
        self.tray_icon_menu.addSeparator()
        self.login = QAction('Login/Sign Up',self)
        self.login.triggered.connect(self.login_menu)
        self.tray_icon_menu.addAction(self.login)
        self.tray_icon_menu.addSeparator()
        self.logout = QAction('Log Out',self)
        self.logout.triggered.connect(self.logout_menu)
        self.tray_icon_menu.addAction(self.logout)
        self.tray_icon_menu.addSeparator()
        exitaction = QAction('Exit',self)
        exitaction.triggered.connect(self.exit_app)
        self.tray_icon_menu.addAction(exitaction)
        self.setContextMenu(self.tray_icon_menu)

    def login_menu(self):
        self.login_window = LoginWindow(self)

    def logout_menu(self):
    	self.storage.delete_login_token()
    	self.storage.delete_saved_password()
    	self.login_window.sync.sync_thread_flag = 0


    def show_note_menu(self,session_num = 1):   # To separate thread function from show_note function
        global note_visible_flag
        if(self.show_note(session_num) == False):
            return
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
            return False
        self.page.updatePage(self.status, self.hashed_key, self.process_name, self.window_title)
        self.note_window.page().runJavaScript(str("firepad.setHtml('"+self.default_text+"')"))
        #self.page.updatePage(self.status, self.hashed_key, self.process_name, self.window_title)
        

    def exit_app(self):
        global window_change_event_flag
        window_change_event_flag = 0
        self.wirm.active_window_thread_flag = 0
        self.internet_check_thread_flag = 0
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
            if(len (note.text) == 1):   # No merge conflict to resolve
                for text in list(note.text.values()):
                    self.default_text = text
            else:   # Merge conflict
                self.note_window.setVisible(False)
                conflict_msg_box = ConflictMsgBox(self, note, self.window_title, self.hashed_key, self.process_name)
                return False
                
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

