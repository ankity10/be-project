import threading
import time
import datetime
import logging
import requests
import json

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from socketcluster import Socketcluster
from storage.storage import *

global IP
IP = "192.168.0.109"
global PORT
PORT = "8000"

receive = "msg_from_server"
send = "msg_from_client"
authentication = "auth"
set_client_id = "set-client-id"


class sync:
    def __init__(self, main_app):
        print("sync started")
        self.send_offline_logs_flag = 0
        self.logout_flag = False  # if client has explicitly logged out
        self.log_count = 0
        self.main_app = main_app
        self.sync_thread_flag = 1
        self.socket = None
        t = threading.Thread(target=self.sync_event)
        t.start()

    def disconnect(self):
        self.logout_flag = True
        self.socket.disconnect()

    def send_offline_logs(self):
        print("log sending started")
        while (self.send_offline_logs_flag == 1):
            if (self.main_app.internet_on_flag == 0):
                self.socket.disconnect()
                self.main_app.logout.setVisible(False)
                self.main_app.login.setVisible(True)
                return
            log_collection = self.main_app.storage.log_collection.find({})
            for log in log_collection:
                print("Log : ", log)
                cont_flag = 0
                json_log = json.loads('{}')
                json_log["note_text"] = log['note_text']
                json_log["process_name"] = log['process_name']
                json_log["note_hash"] = log['note_hash']
                json_log["from_client_id"] = log['from_client_id']
                json_log["window_title"] = log['window_title']
                print("str of log is ", json.dumps(json_log, sort_keys=True))
                try:
                    self.socket.emit(send, json.dumps(json_log, sort_keys=True))
                    print("log sent")
                    self.main_app.storage.delete_log(log['note_hash'])
                except:
                    print("Socket not created")
                    break

    def onmessage(self, eventname, data, ackmessage):
        print("on messsage got called")
        # online_log = json.dumps(data,sort_keys=True)
        if (data != None):
            print("on message got called")
            online_log = data
            print(online_log)
            # return
            # if(online_log['conflict_flag'] == True):	#Conflict has been resolved by some client
            local_log = self.main_app.storage.read_log(str(online_log['note_hash']))
            old_note = self.main_app.storage.read_note(str(online_log['note_hash']))

            if (old_note == None):  # No note stored for that hash
                note_dict = {"create_time": datetime.datetime.now().time().isoformat(),
                             "note_text": online_log["note_text"],
                             "process_name": online_log["process_name"],
                             "window_title": online_log["window_title"],
                             "note_hash": online_log["note_hash"]}
                self.main_app.storage.insert_note(Note(**note_dict))
            else:  # Note is stored for that hash
                if (local_log == None):  # No local log present corresponding to the hash
                    # new_text = {from_client_id : online_log['note_text']}
                    new_note = old_note
                    new_note["note_text"] = online_log['note_text']
                    # note = Note(**old_note)
                    self.main_app.storage.update_note(new_note)
                else:  # Local log present corresponding to the hash
                    old_note = self.main_app.storage.read_note(str(online_log['note_hash']))
                    new_text = self.main_app.merge(old_note['note_text'], online_log['note_text'])
                    # new_text = {from_client_id : online_log['note_text'],self.main_app.client_id : local_log["text"]}
                    new_note = old_note
                    new_note["note_text"] = new_text
                    local_log.note_text = new_text
                    self.main_app.storage.update_log(local_log)
                    self.main_app.storage.update_note(new_note)

        ackmessage(None, True)
        self.main_app.show_note()

        if (self.log_count > 0):
            self.log_count -= 1
        if (self.log_count == 0):  # All logs which were present while offline have been retrieved
            self.send_offline_logs_flag = 1
            t = threading.Thread(target=self.send_offline_logs)
            t.start()
            self.log_count -= 1

    def ack(self, eventname, error, object):
        print("Got ack daata " + str(object) + " and error " + error + "and eventname is " + eventname)

    def onconnect(self, socket):
        logging.info("connected")

    def ondisconnect(self, socket):
        msg_box = QMessageBox()
        logging.info("on disconnect got called")
        self.sync_thread_flag = 0
        self.send_offline_logs_flag = 0
        self.main_app.logout.setVisible(False)
        self.main_app.login.setVisible(True)
        self.send_offline_logs_flag = 0
        if (self.logout_flag == False):  # log_out flag checks if logout has been clicked by the user or server crashed
            self.main_app.message_box("Server is offline!!")

    def onConnectError(self, socket, error):
        logging.info("On connect error got called")

    def onSetAuthentication(self, socket, token):  # called after token is set from server side
        logging.info("Token received " + token)

    # socket.setAuthtoken(token)

    def on_auth_success(self, event, data):
        self.socket.emit("set-client-id", self.main_app.client_id)
        print("client auth success")
        logging.info("Auth Success")
        if (self.log_count == 0):
            self.send_offline_logs_flag = 1
            t = threading.Thread(target=self.send_offline_logs)
            t.start()
            self.log_count -= 1

    def on_disconnect(self, event, data):
        self.send_offline_logs_flag = 0

    def onAuthentication(self, socket, isauthenticated):
        logging.info("Authenticated is " + str(isauthenticated))
        time.sleep(1)
        socket.emit(authentication, self.main_app.login_credentials.token)
        if (self.main_app.login_credentials.token == "0"):
            print("in if")
            self.send_offline_logs_flag = 0
            return
        print("not in if")
        socket.on("#disconnect", self.on_disconnect)
        socket.on("auth-success", self.on_auth_success)
        socket.onack(receive, self.onmessage)

    def sync_event(self):
        message_box = QMessageBox()
        while (self.sync_thread_flag == 1):
            if (self.main_app.internet_on_flag == 1):  # internet on
                self.socket = socket = Socketcluster.socket("ws://" + IP + ":" + PORT + "/socketcluster/")
                socket.setreconnection(False)
                self.log_count = 0
                # Retrieve log_count
                try:
                    self.log_count_response = requests.get(self.main_app.log_count_retrieval_url
                                                           + self.main_app.storage.read_saved_password().username + ":"
                                                           + str(self.main_app.client_id),
                                                           headers={"Authorization": "JWT "
                                                                                     + self.main_app.login_credentials.token})
                except:
                    self.main_app.message_box("Server is offline!!")
                    self.main_app.login.setVisible(True)
                    self.main_app.logout.setVisible(False)
                    return
                if (self.log_count_response.text == "Unauthorized"):  # Invalid token in requests
                    print("Unauthorized!!!")
                    continue
                self.log_count_response = self.log_count_response.json()
                if (self.log_count_response["success"] == 0):
                    print(self.log_count_response["message"])
                    continue
                print(self.log_count_response)
                self.log_count = self.log_count_response["message_count"]
                try:
                    socket.setBasicListener(self.onconnect, self.ondisconnect, self.onConnectError)
                    socket.setAuthenticationListener(self.onSetAuthentication, self.onAuthentication)
                    socket.connect()
                except:
                    print("Server offline!!")
                    continue
            else:
                try:
                    socket.disconnect()
                except:
                    continue
                self.send_offline_logs_flag = 0
        self.send_offline_logs_flag = 0

    def fail_msg_btn(self):
        return
