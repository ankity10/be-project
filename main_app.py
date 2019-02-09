#!/usr/bin/env python3
import datetime
import hashlib
import logging
import os
import sys
import threading
import time
import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from dateutil.relativedelta import relativedelta
from random import randint

from ui.qt.login_window import Ui_Login_Window
from ui.qt.reminder_msg_window import Ui_Rem_MSG_Window
from ui.qt.help_window import Ui_Help_Window
# sudo apt-get install python3-dateutil

from sync.sync import sync
from reminder.reminder import *
from functools import partial


from merge import merge as Merge
from reminder.reminder import *
from sync.sync import sync
from storage.storage import Db
from storage.storage import Local_Log
from storage.storage import Note
from utils.title_processing import TitleProcessing
from wirm.wirm import WIRM

global IP

IP = "192.168.0.109"

global PORT
PORT = "8000"

logging.getLogger('requests').setLevel(logging.CRITICAL)  # Display logs of critical type only
note_visible_flag = 0
window_change_event_flag = 0
APP_NAME = "Notelet"


class WebPage(QWebEnginePage):
    def __init__(self, main_app, status, note_hash, process_name, window_title):
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
                self.save_note(msg[index + 1:])
        except Exception as e:
            print("JavaScript error==>", msg, " at linenumber=", linenumber, " source id = ", source_id)

    def save_note(self, msg):
        try:
            # print(" before escaping",msg)
            # msg = msg.encode("string-escape")
            # print("after escaping", msg)
            note_dict = {"create_time": datetime.datetime.now().time().isoformat(),
                         "note_text": msg,
                         "process_name": self.process_name,
                         "window_title": self.window_title,
                         "note_hash": self.note_hash}
            note = Note(**note_dict)
            local_log_dict = {}
            #############################################
            # if(self.main_app.internet_on_flag != 1 or self.main_app.login_credentials.token == 0):
            local_log_dict = {"note_hash": self.note_hash,
                              "note_text": msg,
                              "process_name": self.process_name,
                              "window_title": self.window_title,
                              "from_client_id": self.main_app.client_id}
            # else:
            # local_log_dict = {"note_hash" :self.note_hash,"text" :msg}

            local_log = Local_Log(**local_log_dict)
            if (self.storage.read_log(self.note_hash) == None):
                self.storage.insert_log(local_log)
            else:
                self.storage.update_log(local_log)
            if self.status == "new":
                self.storage.insert_note(note)
                self.status = "old"
                print("new note inserted")
            elif self.status == "old":
                self.storage.update_note(note)
        except OSError:
            pass  # replace this with error handeling
            # system related error


class NoteWindow(QWebEngineView):
    def __init__(self):
        global window_change_event_flag
        super().__init__()
        file_path = '/ui/notes/examples/richtext-simple.html'
        folder_path = os.path.abspath('./')
        # flags = flags | Qt.WindowStaysOnTopHint 
        # flags = flag | ~Qt.WindowTitleHint
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.abs_path = "file://" + folder_path + file_path
        self.setWindowTitle("Notelet")
        self.setWindowIcon(QIcon('graphics/notes.png'))
        self.load(QUrl(self.abs_path))
        self.setVisible(False)
        self.child = None
        window_change_event_flag = 0
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.min_dist = 5
        self.mouse_press_pos = None
        self.mouse_move_pos = None
        self.mouse_press_x = 0
        self.cursor = QCursor()

    def closeEvent(self, event):
        global note_visible_flag
        self.setVisible(False)
        note_visible_flag = 0
        event.ignore()

class Reminder_Msg_Window(QDialog):
    def __init__(self, main_app):
        super().__init__()
        self.reminder_msg_ui = Ui_Rem_MSG_Window()
        self.reminder_msg_ui.setupUi(self)
        self.main_app = main_app
        # self.reminder_msg_ui.dismiss_button.setCheckable(True)
        # self.reminder_msg_ui.snooze_button.setCheckable(True)
        self.reminder_msg_ui.dismiss_button.clicked.connect(self.dismiss_method)
        self.reminder_msg_ui.snooze_button.clicked.connect(self.snooze_method)
        flags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.tick)
        # self.timer.start(10000)
        self.setWindowFlags(flags)

    # def tick(self):
    #     self.snooze_method()

    def dismiss_method(self):
        print("In dismiss")
        self.main_app.dismiss_checked = True
        self.main_app.snooze_checked = False
        self.close()

    def snooze_method(self):
        print("In snooze")
        self.main_app.dismiss_checked = False
        self.main_app.snooze_checked = True
        self.close()


class LoginWindow(QWidget):
    def __init__(self, main_app, visible_flag=True):
        super().__init__()
        self.flag = 1
        self.main_app = main_app
        self.visible_flag = visible_flag
        self.login_ui = Ui_Login_Window()
        self.login_ui.setupUi(self)
        self.setWindowTitle("LOGIN IN")
        self.login_ui.login_link.hide()
        self.login_ui.signup_button.hide()
        self.login_ui.login_button.clicked.connect(self.login_method)
        self.login_ui.login_link.clicked.connect(self.back_method)
        self.login_ui.signup_button.clicked.connect(self.signup_method)
        self.login_ui.signup_link.clicked.connect(self.signup_ui)
        self.login_ui.signup_label.hide()
        self.login_ui.login_link.hide()
        self.setFixedSize(430, 300)

        self.move(QApplication.desktop().screen().rect().center()- self.rect().center())
        # self.setGeometry(400,250,400,200)
        # self.setWindowTitle('Login/Sign Up')
        # self.username_lbl = self.create_label(5,5,"Username")
        # self.username = self.create_LineEdit(110,5,"Username",285)

        # self.password_lbl = self.create_label(5,30,"Password :")
        # self.password = self.create_LineEdit(110, 30, "Password",285)

        # self.password.setEchoMode(2)

        self.main_app.merge = Merge.merge
        self.setVisible(visible_flag)

    # def reminder_method(self):
    #     print("Start")
    #     self.main_app.reminder = Reminder(self.main_app)

    def create_LineEdit(self, pos_x, pos_y, e_text, e_width):
        line_edit = QLineEdit(self)
        line_edit.setPlaceholderText(e_text)
        line_edit.setMinimumWidth(e_width)
        line_edit.move(pos_x, pos_y)
        return line_edit

    def create_label(self, pos_x, pos_y, l_text):
        label = QLabel(l_text, self)
        label.move(pos_x, pos_y)
        return label

    def create_button(self, b_name, func_name, pos_x, pos_y):
        button = QPushButton(b_name, self)
        button.move(pos_x, pos_y)
        button.clicked.connect(func_name)
        return button

    def back_method(self):
        # self.email_lbl.hide()
        # self.email.hide()
        self.login_ui.login_label.show()
        self.login_ui.signup_label.hide()
        self.login_ui.signup_button.hide()
        self.login_ui.signup_link.show()
        self.login_ui.login_button.show()
        self.login_ui.login_link.hide()
        self.setWindowTitle("LOGIN IN")

    def login_method(self):
        self.username_text = self.login_ui.username.text()
        self.password_text = self.login_ui.password.text()
        print("username :" + self.username_text)
        print("password :" + self.password_text)
        try:
            login_response = requests.post(self.main_app.login_url,
                                           data={'username': self.username_text,
                                                 'password': self.password_text,
                                                 'client_id': self.main_app.client_id}).json()
        except:
            self.main_app.message_box("Server is Offline!!")
            self.main_app.login.setVisible(True)
            self.main_app.logout.setVisible(False)
            return
        self.authentication_flag = login_response["success"]
        if (self.authentication_flag == 0):
            print("in if")
            self.main_app.message_box("Wrong Username or Password!!", self.auth_fail_msg_btn)
            self.clear_textedit()
            self.main_app.login.setVisible(True)
            self.main_app.logout.setVisible(False)
        else:
            self.token = login_response["token"]
            print("Token " + str(self.token))
            self.main_app.login_credentials.token = self.token
            self.main_app.storage.update_login_token(self.token)
            self.is_new = login_response["is_new"]
            self.main_app.storage.insert_saved_password(self.username_text, self.password_text)
            print("is_new = ", self.is_new)
            if (self.is_new == 1):  # New Client
                try:
                    notes_dict = requests.get(str(self.main_app.notes_retrieve_url),
                                              headers={"Authorization": "JWT " + self.token}).json()['notes']
                except:
                    self.main_app.message_box("Server is Offline!!")
                    print("Hello")
                    return
                for note in notes_dict:
                    note_dict = {"create_time": datetime.datetime.now().time().isoformat(),
                                 "note_text": note["note_text"],
                                 "process_name": note["process_name"],
                                 "window_title": note["window_title"],
                                 "note_hash": note["note_hash"]}
                    note_hash = note["note_hash"]
                    window_title = note["window_title"]
                    process_name = note["process_name"]
                    note_text = note["note_text"]
                    old_note = self.main_app.storage.read_note(note_hash)
                    if (old_note == None):  # No note is present for that hash in local db
                        note = Note(**note_dict)
                        self.main_app.storage.insert_note(note)
                    else:  # Note is present for that hash in local db
                        merged_text = self.main_app.merge(note_text, old_note.note_text)
                        old_note.note_text = merged_text
                        self.main_app.storage.update_note(old_note)
                        self.main_app.storage
                        old_log = self.main_app.storage.read_log(note_hash)
                        if (old_log != None):
                            old_log.note_text = merged_text
                            self.main_app.storage.update_log(old_log)
            print("login successful")
            self.main_app.sync = sync(self.main_app)
            self.main_app.login.setVisible(False)
            self.main_app.logout.setVisible(True)
            self.close()

    def auth_fail_msg_btn(self):
        self.flag = 0
        self.show()

    def signup_ui(self):
        self.login_ui.login_link.show()
        self.setWindowTitle("SIGN UP")
        # self.email_lbl.show()
        # self.email.show()
        self.login_ui.signup_button.show()
        self.login_ui.login_button.hide()
        self.login_ui.signup_link.hide()
        self.login_ui.signup_label.show()
        self.login_ui.login_label.hide()

    def signup_method(self):
        self.new_username = self.login_ui.username.text()
        self.new_password = self.login_ui.password.text()
        # self.new_email = self.email.text()
        client_details = self.main_app.storage.read_login_credentials()
        client_id = client_details.client_id
        response = requests.post(self.main_app.signup_url,
                                 json={'username': self.new_username,
                                       'password': self.new_password,
                                       'client_id': client_id})

        data = response.json()
        print(data)
        if ('success' in data):
            new_token = data['token']
            self.main_app.login_credentials.token = new_token
            self.main_app.storage.update_login_token(new_token)
            self.main_app.storage.insert_saved_password(self.new_username, self.new_password)
            self.main_app.message_box("Signed Up successfully!!", self.clear_textedit)
            self.main_app.init_login()
            self.close()
        else:
            err_msg = data['errors']['username']['message']
            self.main_app.message_box(err_msg, self.clear_textedit)

    def clear_textedit(self):
        self.login_ui.username.clear()
        # self.email.clear()
        self.login_ui.password.clear()
class Help_Window(QWidget):
    def __init__(self):
        super().__init__()
        menu = QMenu()

        self.help_ui = Ui_Help_Window()
        self.help_ui.setupUi(self)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, 60)
        self.help_ui.about_edit.hide()
        self.help_ui.shortcut_edit.hide()
        self.help_ui.tips_edit.hide()
        self.help_ui.about_button.setCheckable(True)
        self.help_ui.shortcut_button.setCheckable(True)
        self.help_ui.tips_button.setCheckable(True)
        self.help_ui.shortcut_button.setChecked(True)
        self.is_shortcuts_Checked()
        self.help_ui.about_button.clicked.connect(self.is_about_Checked)
        self.help_ui.shortcut_button.clicked.connect(self.is_shortcuts_Checked)
        self.help_ui.tips_button.clicked.connect(self.is_tips_checked)
        self.move(QApplication.desktop().screen().rect().center()- self.rect().center())

    def is_tips_checked(self):
        if(self.help_ui.tips_button.isChecked()):
            self.help_ui.shortcut_button.setChecked(False)
            self.help_ui.about_button.setChecked(False)
            self.help_ui.tips_edit.show()
            self.help_ui.shortcut_edit.hide()
            self.help_ui.about_edit.hide()

        

    def is_about_Checked(self):
        if(self.help_ui.about_button.isChecked()):
            self.help_ui.shortcut_button.setChecked(False)
            self.help_ui.tips_button.setChecked(False)
            self.help_ui.about_edit.show()
            self.help_ui.shortcut_edit.hide()
            self.help_ui.tips_edit.hide()

    def is_shortcuts_Checked(self):
        if(self.help_ui.shortcut_button.isChecked()):
            self.help_ui.about_button.setChecked(False)
            self.help_ui.tips_button.setChecked(False)
            self.help_ui.about_edit.hide()
            self.help_ui.tips_edit.hide()
            self.help_ui.shortcut_edit.show()



class ThemeSelector():
    theme_list = ['white', 'yellow',"skyblue", 'grey', 'green', 'pink', "blue", "teal"]
    availiable_modes = ["random", "process_wise"]

    def __init__(self, mode):
        if mode in ThemeSelector.availiable_modes:
            self.mode = mode
        else:
            raise ValueError("Invalid mode provided, Available modes are : 'random', 'process_wise' ")

    def select_theme(self, process_name=None):
        if self.mode == 'random':
            return self._random_theme_generator()
        else:
            return self._process_wise_theme_generator(process_name)

    def _random_theme_generator(self):
        random_index = randint(0, len(ThemeSelector.theme_list)-1)
        return ThemeSelector.theme_list[random_index]

    def _process_wise_theme_generator(self, process_name):
        if isinstance(process_name, str) and process_name:
            ascii_sum = 0
            for char in process_name:
                ascii_sum = ascii_sum + ord(char)

            index = ascii_sum%len(ThemeSelector.theme_list)
            return ThemeSelector.theme_list[index]
        else:
            raise ValueError("'{}' should be of type 'str'".format(process_name))


class TrayIcon(QSystemTrayIcon):
    def __init__(self):
        self.log_count_retrieval_url = "http://" + IP + ":" + PORT + "/api/rabbitmq/queue/message/count?queue="
        self.notes_retrieve_url = "http://" + IP + ":" + PORT + "/api/notes"
        self.login_url = "http://" + IP + ":" + PORT + "/api/auth/login"
        self.signup_url = "http://" + IP + ":" + PORT + "/api/auth/signup"
        self.msg_box = QMessageBox()
        self.internet_check_thread_flag = 1
        self.new_rem_entry = 0
        # notify2.init("Notelet")
        self.internet_on_flag = -1
        self.recent_reminder = None
        self.win = ""
        self.window_close = True
        super().__init__()
        print("wirm")
        self.storage = Db()
        self.login_credentials = self.storage.read_login_credentials()
        self.client_id = self.login_credentials.client_id
        print("Client id :" + str(self.client_id))
        t = threading.Thread(target=self.internet_check_thread)
        t.start()
        self.setIcon(QIcon('graphics/notes.png'))
        self.activated.connect(self.tray_icon_activated)
        self.show()
        self.x_position = 0
        self.y_position = 0
        self.note_hash = ""
        self.window_title = ""
        self.process_name = ""
        self.default_text = ""
        self.status = ""
        self.note_window = NoteWindow()
        self.create_menu()
        self.init_login()  # Login attempt from stored username & password
        self.reminder_thread_start = 1
        t = threading.Thread(target=self.set_reminder)
        t.start()
        self.page = WebPage(self, self.status, self.note_hash, self.process_name, self.window_title)
        self.note_window.setPage(self.page)
        self.note_window.load(QUrl(self.note_window.abs_path))
        print("--------------------------------------------------------------------")
        self.wirm = WIRM(self)
        self.theme_selector = ThemeSelector("process_wise")
        self.note_window.setVisible(False)
        self.dismiss_checked = False
        self.snooze_checked = False


    def message_box(self, message, func=lambda: print("Closing message box!")):
        print("in message box")
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(str(message))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowTitle("Message")
        msg_box.buttonClicked.connect(func)
        msg_box.exec_()

    def init_login(self):
        print("in init login")
        while (self.internet_on_flag == -1):
            continue
        if (self.internet_on_flag == 0):
            self.logout.setVisible(False)
        else:
            saved_password = self.storage.read_saved_password()
            if (saved_password == None):
                self.logout.setVisible(False)
            else:
                print("Logging in From saved password")
                login_window = LoginWindow(self, False)
                login_window.login_ui.username.setText(saved_password.username)
                login_window.login_ui.password.setText(saved_password.password)
                login_window.login_method()

    def set_reminder(self):
        while (self.reminder_thread_start == 1):
            print("----------------In thread-----------")
            reminder = self.storage.read_reminder()
            self.recent_reminder = reminder
            print(self.recent_reminder)
            if (reminder):
                print("---------------reminder------------------")
                print(reminder.target_date)
                target_date = datetime.datetime.strptime(reminder.target_date, '%m-%d-%Y').date()
                target_time = datetime.datetime.strptime(reminder.target_time, '%H-%M').time()
                while (QDate.currentDate().toPyDate() < target_date and self.reminder_thread_start == 1):
                    if (self.new_rem_entry == 1):
                        self.reminder_thread_start = 0
                    time.sleep(5)
                    print("---------------current_date-------------")
                    print(QDate.currentDate().toPyDate())
                print("---------------Date-----------")
                current_time = QTime.currentTime().toPyTime()
                while (current_time.hour < target_time.hour and self.reminder_thread_start == 1):
                    if (self.new_rem_entry == 1):
                        self.reminder_thread_start = 0
                    if ((target_time.hour - current_time.hour) > 1):
                        time.sleep(5)
                    else:
                        time.sleep(5)
                    current_time = QTime.currentTime().toPyTime()
                print("--------------Hour-----------")
                current_time = QTime.currentTime().toPyTime()

                while (current_time.minute < target_time.minute and self.reminder_thread_start == 1):
                    if (self.new_rem_entry == 1):
                        self.reminder_thread_start = 0
                    time.sleep(3)
                    current_time = QTime.currentTime().toPyTime()
                print("-----------Minute----------")

                if(current_time.minute >= target_time.minute and self.reminder_thread_start == 1):
                    print("------------IN time-----------")
                    # n = notify2.Notification("Reminder","It's time")
                    # n.show()
                # if(current_time.minute == target_time.minute):
                    # msg = QMessageBox()
                    # msg.setText("Its time")
                    # msg.setStandardButtons(QMessageBox.Ok)
                    # # msg.buttonClicked.connect(self.close_thread)
                    # msg.exec_()
                    # self.reminder_msg_obj.reminder_msg_ui.reminder_msg_edit.setText(reminder.event_name)

                    reminder_msg_obj = Reminder_Msg_Window(self)
                    reminder_msg_obj.reminder_msg_ui.reminder_msg_edit.setText(reminder.event_name)
                    reminder_msg_obj.reminder_msg_ui.window_title.setText(reminder.window_title)
                    reminder_msg_obj.reminder_msg_ui.process_name.setText(reminder.process_name)

                    reminder_msg_obj.reminder_msg_ui.reminder_msg_edit.setAlignment(Qt.AlignCenter)
                    reminder_msg_obj.move(QApplication.desktop().screen().rect().center().x()- reminder_msg_obj.rect().center().x(), 0)
                    reminder_msg_obj.exec_()
                    # del reminder_msg_obj


                # if(self.repetition_text != 0):
                #   self.repetition_selection_method()
                #   self.set_reminder()
                    if(reminder.repetition != 0 and self.dismiss_checked):
                        if(reminder.repetition == 1):

                            target_date = target_date + datetime.timedelta(days=1)
                        elif (reminder.repetition == 2):
                            target_date = target_date + datetime.timedelta(days=7)
                        elif (reminder.repetition == 3):
                            target_date = target_date + relativedelta(months=1)
                        print("----------updated date is----------")
                        print(target_date)
                        target_date_string = target_date.strftime('%m-%d-%Y')
                        reminder.target_date = target_date_string
                        self.storage.update_reminder(reminder.note_hash, reminder.event_name, reminder)
                    elif(self.dismiss_checked):
                        self.storage.delete_reminder(reminder.note_hash, reminder.target_date, reminder.target_time)
                    elif(self.snooze_checked):
                        print("Snoozing-------------")
                        target_time = datetime.datetime.now() + datetime.timedelta(minutes= 5)
                        target_time_string = target_time.strftime('%H-%M')
                        reminder.target_time = target_time_string
                        self.storage.update_reminder(reminder.note_hash, reminder.event_name, reminder)

                if(self.new_rem_entry == 1):

                    self.new_rem_entry = 0
                    self.reminder_thread_start = 1
                    # reminder = self.storage.read_reminder()
            else:
                print("------------No entry in database-----------")
                self.dismiss_checked = False
                self.snooze_checked = False
                self.recent_reminder = None
                self.reminder_thread_start = 0
        print("-----------------reminder thread stopped----------------")

    def internet_check_thread(self):
        while (self.internet_check_thread_flag == 1):
            if (self.internet_on() == True):
                self.internet_on_flag = 1
            else:
                self.internet_on_flag = 0
            time.sleep(1)

    def internet_on(self):
        try:
            response = requests.get('http://google.com')
            return True
        except:
            pass
            return False

    def create_menu(self):
        self.tray_icon_menu = QMenu()
        self.shownote = QAction(' Show Note', self, checkable=True)
        self.shownote.triggered.connect(self.isChecked)
        self.tray_icon_menu.addAction(self.shownote)
        self.tray_icon_menu.addSeparator()
        self.login = QAction('Login/Sign Up', self)
        self.login.triggered.connect(self.login_menu)
        self.tray_icon_menu.addAction(self.login)
        self.tray_icon_menu.addSeparator()
        self.logout = QAction('Log Out', self)
        self.logout.triggered.connect(self.logout_menu)
        self.tray_icon_menu.addAction(self.logout)
        self.tray_icon_menu.addSeparator()

        self.reminder_option = QAction('Reminder', self)
        self.reminder_option.triggered.connect(self.start_reminder_ui)
        self.tray_icon_menu.addAction(self.reminder_option)
        self.tray_icon_menu.addSeparator()
        self.help_option = QAction('Help', self)
        self.help_option.triggered.connect(self.help_method)
        self.tray_icon_menu.addAction(self.help_option)
        self.tray_icon_menu.addSeparator()
        # self.close_window.setVisible(False)
        exitaction = QAction('Exit', self)

        exitaction.triggered.connect(self.exit_app)
        self.tray_icon_menu.addAction(exitaction)
        self.setContextMenu(self.tray_icon_menu)

    def help_method(self):
        # if(self.help_option.isChecked()):
        self.help_ui = Help_Window()
        self.help_ui.setVisible(True)
        # else:
        #     self.help_ui.setVisible(False)

    def isChecked(self):
        if (self.shownote.isChecked()):
            # self.shownote.setCheckable(True)
            self.show_note_menu(0)
        else:
            # self.shownote.setCheckable(False)
            self.note_window.setVisible(False)

    def start_reminder_ui(self):
        self.reminder = Reminder(self)

    def login_menu(self):
        if (self.internet_on_flag == 0):
            self.message_box("You are offline!!")
        else:
            self.login_window = LoginWindow(self)

    def logout_menu(self):
        self.storage.delete_login_token()
        self.storage.delete_saved_password()
        self.logout.setVisible(False)
        self.login.setVisible(True)
        self.sync.send_offline_logs_flag = 1
        self.sync.sync_thread_flag = 0
        self.sync.disconnect()
        self.message_box("Logged out successfully!")

    # def close_window_method(self):
    #     self.note_window.close()
    #     self.close_window.setVisible(False)


    def show_note_menu(self, session_num=1):  # To separate thread function from show_note function
        # self.note_window.page().runJavaScript("init()")
        # self.close_window.setVisible(True)
        global note_visible_flag
        if (self.show_note(session_num) == False):
            return
        self.set_position()

    def set_position(self):
        if self.x_position == 0:
            position = self.geometry().topRight()
            self.x_position = int(position.x())
            self.y_position = int(position.y())
            if self.x_position <= 0:
                self.x_position = QCursor().pos().x()
                self.y_position = QCursor().pos().y()
            print(self.x_position, self.y_position)
            self.note_window.setGeometry(self.x_position, self.y_position, 280, 310)
        self.note_window.setVisible(True)
        note_visible_flag = 1

    def show_note(self, session_num=1):  # sesion_num = 0 when note option is clicked(for xfce), else 1
        global note_visible_flag
        if (self.get_note(session_num) == False):
            return False
        self.page.updatePage(self.status, self.note_hash, self.process_name, self.window_title)
        self.format_note()
        js_cmd = str("firepad.setHtml('" + self.default_text + "')")
        self.note_window.page().runJavaScript(js_cmd)
        theme = self.theme_selector.select_theme(self.process_name)
        print("Theme: ", theme)
        theme_cmd = "setTheme('"+theme+"');"
        self.note_window.page().runJavaScript(theme_cmd)


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
        self.reminder_thread_start = 0

        try:
            self.sync.disconnect()
            self.sync.sync_thread_flag = 0
            self.sync.send_offline_logs_flag = 0
        except:
            pass
        sys.exit(0)

    def calc_hash(self, **kwargs):
        sha256 = hashlib.sha256()
        sha256.update((kwargs['process_name'] + kwargs['window_title']).encode('utf-8'))
        note_hash = sha256.hexdigest()
        return note_hash

    def get_note(self, session_num=1):
        global APP_NAME
        while (self.wirm.active_window_thread_flag == 0):
            continue
        self.window_title = str(self.wirm.get_active_window_title(session_num))
        self.process_name = self.wirm.get_active_window_name(session_num)
        if (self.window_title == APP_NAME and session_num == 0):
            return False
        elif (self.window_title == APP_NAME and session_num == 1):
            print(APP_NAME)
            self.window_title = self.wirm.prev_active_window_title
            self.process_name = self.wirm.prev_active_window_name

        '''
        if self.process_name in ["sublime_text", "subl"]:
            print("Entered sublime_text condition")
            
            prev_clip = pyperclip.paste()
            pyperclip.copy("")
            time.sleep(0.5)
            subprocess.call(["xdotool", "windowfocus", str(self.wirm.active_window_id)])
            subprocess.call(["xdotool", "key", "ctrl+shift+l"])  #Call the sublime plugin for filepaths
            # time.sleep(0.5)
            filepath = pyperclip.paste()          

            if(filepath == ""):
                print("Plugin doesn't exist")
            else:                
                print("Filepath from sublime: ", filepath)
                self.window_title = filepath       

            pyperclip.copy(prev_clip)
        '''
        title_processing_obj = TitleProcessing(self.process_name, self.window_title)
        self.window_title = title_processing_obj.get_path()

        self.note_hash = self.calc_hash(process_name=self.process_name, window_title=self.window_title)
        # print("note_hash "+self.note_hash)
        # print(self.window_title)
        print("Window title :", self.window_title)
        print("Process name :", self.process_name)
        self.note_hash = self.calc_hash(process_name=self.process_name, window_title=self.window_title)
        # print("note_hash "+self.note_hash)
        note = self.storage.read_note(self.note_hash)
        if note:
            self.default_text = note.note_text
            self.status = "old"
        else:
            self.default_text = ""
            self.status = "new"
        return True


    def tray_icon_activated(self, reason):
        self.window_close = not self.window_close
        if (reason == QSystemTrayIcon.Trigger):
            if (not self.window_close):
                self.show_note_menu(0)
                self.note_window.setVisible(True)
                self.shownote.setChecked(True)
            else:
                self.note_window.setVisible(False)
                self.shownote.setChecked(False)
                # self.close_window.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    trayicon = TrayIcon()
    app.exec_()
