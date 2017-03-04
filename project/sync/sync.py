import urllib.error
import threading
import asyncio
import websockets
import time
import datetime
import requests

from PyQt5.QtWidgets import *
from socketclusterclient import Socketcluster
from storage.storage2 import *

class sync:

	def __init__(self, main_app):
		self.internet_on_flag = False
		self.send_offline_logs_flag = 0
		self.log_count = 0
		self.main_app = main_app
		self.sync_thread_flag = 1
		t = threading.Thread(target=self.sync_event)
		t.start()

	# def client_online_thread(self):
	# 	asyncio.get_event_loop().run_until_complete(self.client_online())

	# def client_online(self):
	# 	async with websockets.connect('ws://localhost:8765') as websocket:
	# 		self.retrieve_online_logs(websocket)
	# 		self.send_offline_logs(websocket)

	# def retrieve_online_logs(self,websocket):
	# 	websocket.send("ready")
	# 	log_number = int(websocket.recv())
	# 	if(log_number == 0):
	# 		return
	# 	else:
	# 		for i in range(1,log_number): 
	# 			log = websocket.recv()
	# 			if(log['conflict_flag'] == True):
	# 				local_log = self.main_app.storage.read_log(str(log['note_hash']))
	# 				if(local_log == None):
	# 					old_note = self.storage.read_note(str(log['note_hash']))
	# 					#self.main_app.storage.insert_note()
	# 	                old_text = old_note["text"]
	# 	               	# note_dict["text"] = old_text
	# 	                old_text["text"][log['from_client_id']] = log['note_text']
	# 	                note = Note(**note_dict)
	# 	                self.storage.update_note(note)


	def send_offline_logs(self,websocket):
		while(self.send_offline_logs_flag == 1):
			log_collection = self.main_app.storage.log_collection.find({})
			delete_count = self.main_app.storage.log_collection.delete_many({}) 
			for log in log_collection:
				websocket.emit('sendmsg',log)
				print("log sent")		

	# def internet_on():
	#     for timeout in [1,5,10,15]:
	#         try:
	#             response=urlopen('http://google.com',timeout=timeout)
	#             return True
	#         except urllib.error.URLError as err: pass
	#     return False
##########################################################################

	def onmessage(self,eventname,data, ackmessage):
		online_log = json.dumps(data,sort_keys=True)
		from_client_id = online_log['from_client_id']
		ackmessage(None, True)
		# if(online_log['conflict_flag'] == True):	#Conflict has been resolved by some client
		local_log = self.main_app.storage.read_log(str(online_log['note_hash']))
		old_note = self.main_app.storage.read_note(str(online_log['note_hash']))
		if(old_note == None):	# No note stored for that hash
			note_dict = {"create_time": datetime.datetime.now().time().isoformat(), "note_text": msg, "process_name": online_log["process_name"], "window_title": online_log["window_title"], "note_hash":online_log["note_hash"]}
			self.main_app.storage.insert_note()
		else:	#Note is stored for that hash
			if(local_log == None):	#No local log present corresponding to the hash
				old_note = self.main_app.storage.read_note(str(online_log['note_hash']))
				# new_text = {from_client_id : online_log['note_text']}
				old_note["note_text"] = online_log['note_text']
				note = Note(**old_note)
				self.main_app.storage.update_note(note)
			else:	#Local log present corresponding to the hash
				old_note = self.main_app.storage.read_note(str(online_log['note_hash']))
				## new_text = merge(old_note,online_log['note_text'])
				# new_text = {from_client_id : online_log['note_text'],self.main_app.client_id : local_log["text"]}
				old_note["note_text"] = new_text
				note = Note(**old_note)
				self.main_app.storage.update_note(note)
		#  	else:	#Conflict has not been resolved
		#  		old_note = self.main_app.storage.read_note(str(online_log['note_hash']))
				# old_text = old_note["text"]
				# old_text[online_log['from_client_id']] = online_log['note_text']
				# old_note["text"] = old_text
				# note = Note(**old_note)
				# self.storage.main_app.update_note(note)
		if(self.log_count > 0):
			self.log_count -= 1
		if(self.log_count == 0):	#All logs which were present while offline have been retrieved
			self.send_offline_logs_flag = 1
			t = threading.Thread(target=self.send_offline_logs)
			t.start()
			self.log_count -= 1

	def ack(self,eventname, error, object):
	    print("Got ack daata "+str(object)+" and error "+error+ "and eventname is "+ eventname)

	def onconnect(self,socket):
	   logging.info("connected")

	def ondisconnect(self,socket):
	    logging.info("on disconnect got called")

	def onConnectError(self,socket, error):
	    logging.info("On connect error got called")

	def onSetAuthentication(self,socket, token): #called after token is set from server side
	    logging.info("Token received " + token)
	    #socket.setAuthtoken(token)

	def on_auth_success(self,event):
		socket.onack("msg",self.onmessage)

	def on_disconnect(self,event,data):
		self.internet_on_flag = False
		self.send_offline_logs_flag = 0

	def onAuthentication(self,socket, isauthenticated):
		logging.info("Authenticated is " + str(isauthenticated))
		time.sleep(1)
		if(self.main_app.login_credentials.token == "0"):
			self.internet_on_flag = False
			self.send_offline_logs_flag = 0
			return	
		socket.setAuthtoken(self.main_app.login_credentials.token)
		socket.on("#disconnect", self.on_disconnect)
		socket.on("auth-success", self.on_auth_success)

	#################################################################################

	def sync_event(self):
		while(self.sync_thread_flag == 1):
			socket = Socketcluster.socket("ws://localhost:8000/socketcluster/")
			if(self.main_app.internet_on() == True):	#internet on
				self.log_count = 0
				self.internet_on_flag = True

				#Retrieve log_count
				self.log_count_response = requests.get(self.main_app.log_count_retrieval_url+str(self.main_app.client_id),headers={"Authorization" : "JWT "+self.main_app.login_credentials.token})
				if(self.log_count_response.text == "Unauthorized"):
					print("Unauthorized!!!")
					continue
				self.log_count_response = self.log_count_response.json()
				if(self.log_count_response["success"] == 0):
					print(self.log_count_response["message"])
					continue
				print(self.log_count_response)
				return
				socket.setBasicListener(self.onconnect, self.ondisconnect, self.onConnectError)
				socket.setAuthenticationListener(self.onSetAuthentication, self.onAuthentication)
				socket.setreconnection(False)
				socket.connect()
				
			else:
				socket.disconnect()
				self.internet_on_flag = False
				self.send_offline_logs_flag = 0

	def fail_msg_btn(self):
		return	
			