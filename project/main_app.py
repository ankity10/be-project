#!/usr/bin/env python3
import threading
import Xlib.display
import Xlib.threaded
import sys
import requests
import os
import time
import logging
import datetime
import hashlib
import urllib.request
import requests
import json

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

from sync.sync import sync
from functools import partial

from merge import merge as Merge

global IP
IP = "192.168.0.110"
global PORT
PORT = "8000"

logging.getLogger('requests').setLevel(logging.CRITICAL) #Display logs of critical type only
note_visible_flag = 0
window_change_event_flag = 0
APP_NAME = "LazyNotes"




class WebPage(QWebEnginePage):

    def __init__(self,main_app, status, note_hash, process_name, window_title):
        super().__init__()
        self.main_app = main_app
        self.status = status
        self.storage = self.main_app.storage
        self.note_hash = note_hash
        self.process_name = process_name
        self.window_title = window_title

    def updatePage(self, status, note_hash, process_name, window_title):
        self.status = status
        # self.storage = self.main_app.storage
        self.note_hash = note_hash
        self.process_name = process_name
        self.window_title = window_title

    

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):        
        delimeter = "$"
        delimeter_index = 9
        try:
            index = msg.index(delimeter)
            if index == delimeter_index:
                self.save_note(msg[index+1:])
        except Exception as e:
            print("JavaScript error==>",msg, " at linenumber=", linenumber, " source id=", source_id) 
    

    def save_note(self, msg):
        try:
            # print(" before escaping",msg)
            # msg = msg.encode("string-escape")
            # print("after escaping", msg)
            note_dict = {"create_time": datetime.datetime.now().time().isoformat(), "note_text": msg, "process_name": self.process_name, "window_title": self.window_title, "note_hash":self.note_hash}
            note = Note(**note_dict)
            local_log_dict = {}
            #############################################
            # if(self.main_app.internet_on_flag != 1 or self.main_app.login_credentials.token == 0):
            local_log_dict = {"note_hash" :self.note_hash,"note_text" :msg,"process_name": self.process_name, "window_title": self.window_title,"from_client_id" : self.main_app.client_id}
            # else:
            # local_log_dict = {"note_hash" :self.note_hash,"text" :msg}
            local_log = Local_Log(**local_log_dict)
            if(self.storage.read_log(self.note_hash) == None):
                self.storage.insert_log(local_log)
            else:
                self.storage.update_log(local_log)
            #############################################    
            if self.status == "new":
                self.storage.insert_note(note)
                self.status = "old"
                print("new note inserted")
            elif self.status == "old":
                # if(self.main_app.internet_on_flag != 1 or self.main_app.login_credentials.token == 0):
                #     old_note = self.storage.read_note(self.note_hash)
                #     note_dict["text"] = old_note.text
                #     note_dict["text"][str(self.main_app.client_id)] = msg
                # note = Note(**note_dict)
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
        flags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        self.setWindowFlags(flags)
        self.abs_path = "file://" + folder_path + file_path
        self.setWindowTitle("LazyNotes")
        self.setWindowIcon(QIcon('graphics/notes.png'))
        self.load(QUrl(self.abs_path))
       # self.setWindowFlags()
        self.setVisible(False)
        window_change_event_flag = 0

    def closeEvent(self,event):
        global note_visible_flag
        self.setVisible(False) 
        note_visible_flag = 0
        event.ignore()      

class LoginWindow(QWidget):
    
    def __init__(self,main_app,visible_flag = True):
        super().__init__()
        self.flag = 1
        self.main_app = main_app
        self.visible_flag = visible_flag
        #self.setMinimumSize(200, 400)
        self.setGeometry(400,250,400,200)
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
        self.email_lbl = QLabel("Email:", self)
        self.email_lbl.move(5, 55)
        self.email_lbl.hide()
        self.email = QLineEdit(self)
        self.email.setPlaceholderText('Email')
        self.email.setMinimumWidth(285)
        self.email.move(110, 55)
        self.email.hide()
        self.login_button = QPushButton("Log In",self)
        self.login_button.move(120,80)
        self.login_button.clicked.connect(self.login_method)
        self.new_user_button = QPushButton("New User?", self)
        self.new_user_button.move(200,80)
        self.new_user_button.clicked.connect(self.signup_ui)
        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.move(200,110)
        self.signup_button.hide()
        self.signup_button.clicked.connect(self.signup_method)
        self.back_button = QPushButton("<-Back", self)
        self.back_button.move(120,110)
        self.back_button.hide()
        self.back_button.clicked.connect(self.back_method)
        self.main_app.merge = Merge.merge
        self.setVisible(visible_flag)

    def back_method(self):
        self.email_lbl.hide()
        self.email.hide()
        self.signup_button.hide()
        self.new_user_button.show()
        self.login_button.show()
        self.back_button.hide()


    def login_method(self):
        # print(self.username.text())
        # print(username)
        # if(username == ""):
        #     print("USER"+str(self.username.text()))
        # else:
        self.username_text = self.username.text()
        self.password_text = self.password.text()  
        print("username :"+self.username_text)
        print("password :"+self.password_text)
        login_response=requests.post(self.main_app.login_url,data = {'username' : self.username_text,'password' : self.password_text,'client_id' : self.main_app.client_id}).json()
        print(login_response)
        self.authentication_flag = login_response["success"] 
        # print("authentication flag = "+str(self.authentication_flag))
        if(self.authentication_flag == 0):
            print("in if")
            self.main_app.auth_fail_msg.setIcon(QMessageBox.Information)
            self.main_app.auth_fail_msg.setText("Wrong User Name or Password!!")
            self.main_app.auth_fail_msg.setStandardButtons(QMessageBox.Ok)
            self.main_app.auth_fail_msg.show()
            self.main_app.auth_fail_msg.buttonClicked.connect(self.auth_fail_msg_btn)
            self.main_app.login.setVisible(True)
            self.main_app.logout.setVisible(False)
        else:
            self.token = login_response["token"]
            print("Token " +str(self.token))
            self.main_app.login_credentials.token = self.token
            self.main_app.storage.update_login_token(self.token)
            self.is_new = login_response["is_new"]
            self.main_app.storage.insert_saved_password(self.username_text, self.password_text)
            print("is_new = ", self.is_new)
            if(self.is_new == 1):   #New Client
                notes_json = requests.get(str(self.main_app.notes_retrieve_url), headers={"Authorization" : "JWT "+self.token}).json()
                print("JSON " + "="*30, notes_json)
                notes_dict = notes_json['notes']
                print("Dict " + "="*30, notes_dict)
                for note in notes_dict:
                    note_dict = {"create_time": datetime.datetime.now().time().isoformat(), "note_text": note["note_text"], "process_name": note["process_name"], "window_title": note["window_title"], "note_hash":note["note_hash"]}
                    note_hash = note["note_hash"]
                    window_title = note["window_title"]
                    process_name = note["process_name"]
                    note_text = note["note_text"]
                    old_note = self.main_app.storage.read_note(note_hash)
                    if(old_note == None):    # No note is present for that hash in local db
                        note = Note(**note_dict)
                        self.main_app.storage.insert_note(note)
                    else:   # Note is present for that hash in local db
                        merged_text = self.main_app.merge(note_text,old_note.note_text)
                        old_note.note_text = merged_text
                        self.main_app.storage.update_note(old_note)
            print("login successful")
            self.main_app.sync = sync(self.main_app)
            self.main_app.login.setVisible(False)
            self.main_app.logout.setVisible(True)
            self.close()

    def auth_fail_msg_btn(self):
        self.flag = 0
        self.show()

    def signup_ui(self):
        self.back_button.show()
        self.email_lbl.show()
        self.email.show()
        self.signup_button.show()
        self.new_user_button.hide()
        self.login_button.hide()

    def signup_method(self):
        self.new_username = self.username.text()
        self.new_password = self.password.text()
        # self.new_email = self.email.text()
        client_details = self.main_app.storage.read_login_credentials()
        client_id = client_details.client_id
        response = requests.post(self.main_app.signup_url, json = {'username': self.new_username, 'password' : self.new_password, 'client' : client_id})
        data = response.json()
        print(data)
        if('success' in data):
            new_token = data['token']
            self.main_app.login_credentials.token = new_token
            self.main_app.storage.update_login_token(new_token) 
            self.main_app.storage.insert_saved_password(self.new_username, self.new_password) 
            signup_success_msg = QMessageBox()
            signup_success_msg.setIcon(QMessageBox.Information)
            signup_success_msg.setText("Signed up successfully")
            signup_success_msg.setStandardButtons(QMessageBox.Ok)
            signup_success_msg.setWindowTitle("Message")
            signup_success_msg.buttonClicked.connect(self.clear_textedit)
            signup_success_msg.exec_()
            self.main_app.login.setVisible(False)
            self.main_app.logout.setVisible(True)
            self.main_app.sync = sync(self.main_app)
            self.close()
        else:
            err_msg = data['errors']['username']['message']
            signup_fail_msg = QMessageBox()
            signup_fail_msg.setIcon(QMessageBox.Information)
            signup_fail_msg.setText(err_msg)
            signup_fail_msg.setStandardButtons(QMessageBox.Ok)
            signup_fail_msg.setWindowTitle("Message")
            signup_fail_msg.buttonClicked.connect(self.clear_textedit)
            signup_fail_msg.exec_()
            

    def clear_textedit(self):
        self.username.clear()
        self.email.clear()
        self.password.clear()



class ConflictResolveWidget(QWidget):
    def __init(self,main_app,note, window_title, note_hash, process_name):
        super().__init__()
        self.window_title = window_title
        self.note_hash = note_hash
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
        local_log_dict = {"note_hash" :self.note_hash,"note_text" :msg,"conflict_flag":True}
        local_log = Local_Log(**local_log_dict)
        if(self.storage.read_log(self.note_hash) == None):
            self.storage.insert_log(local_log)
        else:
            self.storage.update_log(local_log)
        note_dict = {"create_time": datetime.datetime.now().time().isoformat(), "note_text": {self.main_app.client_id : text}, "process_name": self.process_name, "window_title": self.window_title, "note_hash":self.note_hash}
        note = Note(**note_dict)
        self.storage.update_note(note)


class ConflictMsgBox(QMessageBox):
    def __init__(self, main_app, note, window_title, note_hash, process_name):
        super().__init__()
        self.window_title = window_title
        self.note_hash = note_hash
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
                                                                     self.note_hash, self.process_name)


class TrayIcon(QSystemTrayIcon):

    def __init__(self):
        self.auth_fail_msg = QMessageBox()
        self.log_count_retrieval_url = "http://"+IP+":"+PORT+"/api/queue/count?queue="
        self.notes_retrieve_url = "http://"+IP+":"+PORT+"/api/notes"
        self.login_url = "http://"+IP+":"+PORT+"/api/user/auth/login"
        self.signup_url = "http://"+IP+":"+PORT+"/api/user/auth/signup"
        self.internet_on_flag = -1  # = -1 if thread has not checked even once, = 0 if offline, = 1 if online
        self.internet_check_thread_flag = 1
        self.win = ""
        self.window_close = True
        super().__init__()
        print("wirm")
        self.storage = Db()
        self.login_credentials = self.storage.read_login_credentials()
        self.client_id = self.login_credentials.client_id
        print("Client id :"+str(self.client_id))
        t = threading.Thread(target=self.internet_check_thread)
        t.start()
        self.setIcon(QIcon('graphics/notes.png'))
        self.activated.connect(self.tray_icon_activated)
        self.create_menu()
        self.show()
        self.x_position = 0
        self.y_position = 0
        self.thread_scheduler = 0
        self.note_hash = ""
        self.window_title = ""
        self.process_name = ""
        self.default_text = ""
        self.status = ""
        self.note_window = NoteWindow()
        #self.note_window.window_change_event_flag = 0
        self.init_login()   # Login attempt from stored username & password
        self.page = WebPage(self,self.status, self.note_hash, self.process_name, self.window_title)
        self.note_window.setPage(self.page)
        # self.note_window.page().runJavaScript(str())
        self.note_window.load(QUrl(self.note_window.abs_path))
        print("--------------------------------------------------------------------")
        self.wirm = WIRM(self)
        self.note_window.setVisible(False)
        #self.window_change_thread()


    def init_login(self):
        print("in init login")
        while(self.internet_on_flag == -1): #To prevent this function from starting before internet is checked
            continue
        if(self.internet_on_flag == 0):
            self.logout.setVisible(False)
        else:
            saved_password = self.storage.read_saved_password()
            if(saved_password == None):
                self.logout.setVisible(False)
            else:
                print("Logging in From saved password")
                login_window = LoginWindow(self,False)
                login_window.username.setText(saved_password.username)
                login_window.password.setText(saved_password.password)
                login_window.login_method()


    def internet_check_thread(self):
        while(self.internet_check_thread_flag == 1):
            if(self.internet_on() == True):
                self.internet_on_flag = 1
            else:
                self.internet_on_flag = 0
            time.sleep(1)


    def internet_on(self):
        try:
            response=requests.get('http://google.com')
            return True
        except:
            pass
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
        self.close_window = QAction('Close',self)
        self.close_window.triggered.connect(partial(self.close_window_method))
        self.tray_icon_menu.addAction(self.close_window)
        self.tray_icon_menu.addSeparator()
        self.close_window.setVisible(False)
        exitaction = QAction('Exit',self)
        exitaction.triggered.connect(self.exit_app)
        self.tray_icon_menu.addAction(exitaction)
        self.setContextMenu(self.tray_icon_menu)

    def login_menu(self):
        self.login_window = LoginWindow(self)

    def logout_menu(self):
        self.storage.delete_login_token()
        self.storage.delete_saved_password()
        self.logout.setVisible(False)
        self.login.setVisible(True)
        self.sync.sync_thread_flag = 0

    def close_window_method(self):
        self.note_window.close()
        self.close_window.setVisible(False)

    def show_note_menu(self,session_num = 1):   # To separate thread function from show_note function
        # self.note_window.page().runJavaScript("init()")
        self.close_window.setVisible(True)
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
        self.page.updatePage(self.status, self.note_hash, self.process_name, self.window_title)
        self.format_note()
        js_cmd = str("firepad.setHtml('"+self.default_text+"')")
        # print(js_cmd)
        self.note_window.page().runJavaScript(js_cmd)
        # self.note_window.page().runJavaScript(str("firepad.setHtml('"+"sda"+"')"))
        # self.note_window.page().runJavaScript(str("alert()")

 
        #self.page.updatePage(self.status, self.note_hash, self.process_name, self.window_title)
        

    def format_note(self):
        style_tag = "</style>"
        if style_tag in self.default_text:
            # print("present", self.default_text.split("</style>")[1])
            self.default_text = self.default_text.split("</style>")[1]
            self.default_text = self.default_text.replace('"', '\\"')
            self.default_text = self.default_text.strip()

            # print("default text is ", self.default_text)
            # print(type(self.default_text))

        else:
            # print("not resent")
            pass


    def exit_app(self):
        global window_change_event_flag
        window_change_event_flag = 0
        self.wirm.active_window_thread_flag = 0
        self.internet_check_thread_flag = 0

        try:
            self.sync.disconnect()
            self.sync.sync_thread_flag = 0
            
        except:
            pass
        sys.exit(0)

    def calc_hash(self, **kwargs):
        sha256 = hashlib.sha256()
        sha256.update((kwargs['process_name'] + kwargs['window_title']).encode('utf-8'))
        note_hash = sha256.hexdigest()
        return note_hash

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
        self.note_hash = self.calc_hash(process_name = self.process_name,window_title = self.window_title)
        #print("note_hash "+self.note_hash)
        note = self.storage.read_note(self.note_hash)
        if note:
            # #self.default_text = note.note_attr_obj.note_info
            # if(len (note.text) == 1):   # No merge conflict to resolve
            #     for text in list(note.text.values()):
            self.default_text = note.note_text
            # else:   # Merge conflict
            #     self.note_window.setVisible(False)
            #     conflict_msg_box = ConflictMsgBox(self, note, self.window_title, self.note_hash, self.process_name)
            #     return False
            self.status = "old"
        else:
            self.default_text = ""
            self.status = "new"
        return True

    def tray_icon_activated(self, reason):
        self.window_close = not self.window_close
        if(reason == QSystemTrayIcon.Trigger):
            if(not self.window_close):
                self.show_note_menu(0)
            else:
                self.note_window.setVisible(False)
                self.close_window.setVisible(False)


if __name__ == '__main__':
    app=QApplication(sys.argv) 
    app.setQuitOnLastWindowClosed(False)
    trayicon=TrayIcon()
    app.exec_()

