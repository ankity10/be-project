import urllib.error
import threading
import asyncio
import websockets

from storage.storage2 import *
from urllib.request import urlopen

class sync:

	def __init__(self, main_app):
		self.send_offline_logs_flag = 0
		self.log_count = 0
		self.main_app = main_app
		self.sync_thread_flag = 1
		t = threading.Thread(target=self.sync_event)
		t.start()

	def client_online_thread(self):
		asyncio.get_event_loop().run_until_complete(self.client_online())

	async def client_online(self):
		async with websockets.connect('ws://localhost:8765') as websocket:
			self.retrieve_online_logs(websocket)
			self.send_offline_logs(websocket)

	def retrieve_online_logs(self,websocket):
		websocket.send("ready")
		log_number = int(websocket.recv())
		if(log_number == 0):
			return
		else:
			for i in range(1,log_number): 
				log = websocket.recv()
				if(log['conflict_flag'] == True):
					local_log = self.main_app.storage.read_log(str(log['note_hash']))
					if(local_log == None):
						old_note = self.storage.read_note(str(log['note_hash']))
						#self.main_app.storage.insert_note()
		                old_text = old_note["text"]
		               # note_dict["text"] = old_text
		                old_text["text"][log['from_client_id']] = log['note_text']
		                note = Note(**note_dict)
		                self.storage.update_note(note)


	def send_offline_logs(self,websocket):
		while(self.send_offline_logs_flag == 1):
			log_collection = self.main_app.storage.log_collection.find({})
			delete_count = self.main_app.storage.log_collection.delete_many({}) 
			for log in log_collection:
				websocket.emit('sendmsg',log)		

	def internet_on():
	    for timeout in [1,5,10,15]:
	        try:
	            response=urlopen('http://google.com',timeout=timeout)
	            return True
	        except urllib.error.URLError as err: pass
	    return False
##########################################################################

	def onmessage(self,eventname,data, ackmessage):
		#Retrieve log_count

		online_log = json.dumps(data,sort_keys=True)
		from_client_id = online_log['from_client_id']
    	ackmessage(None, True)
    	if(online_log['conflict_flag'] == True):
    		local_log = self.main_app.storage.read_log(str(online_log['note_hash']))
    		if(local_log == None):
    			old_note = self.storage.read_note(str(online_log['note_hash']))
    			new_text = {from_client_id : online_log['note_text']}
    			old_note["text"] = new_text
    			note = Note(**old_note)
    			self.storage.update_note(note)
    		else:
    			old_note = self.storage.read_note(str(online_log['note_hash']))
    			new_text = {from_client_id : online_log['note_text'],self.main_app.client_id : local_log["text"]}
				old_note["text"] = new_text
				note = Note(**old_note)
				self.storage.update_note(note)
    	else:
    		old_note = self.storage.read_note(str(online_log['note_hash']))
			old_text = old_note["text"]
			old_text[online_log['from_client_id']] = online_log['note_text']
			old_note["text"] = old_text
			note = Note(**old_note)
			self.storage.update_note(note)

    	self.log_count -= 1
    	if(self.log_count == 0):
    		self.send_offline_logs_flag = 1
    		t = threading.Thread(target=self.send_offline_logs)
			t.start()
			self.log_count -= 1

	def ack(self,eventname, error, object):
	    print("Got ack daata "+str(object)+" and error "+error+ "and eventname is "+ eventname)

	# def callme(self,socket):
	#     # socket.signedAuthToken("kkjbjyuyvgvgc")
	#     #socket.authToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1ODk4ZDgyMzY4Y2RhZjQ1Y2IyNmU2NjYiLCJfX3YiOjAsImlhdCI6MTQ4NjQxMjI2NSwiZXhwIjoxNDg2NTEyMzQ1fQ.vIRAUMytMiCQiTPOlY6vmoFrJqv7bv1fC-OCzJc9GpA"
	#     #print(socket.authToken)
	#     #socket.emit("login", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1ODk4ZDgyMzY4Y2RhZjQ1Y2IyNmU2NjYiLCJfX3YiOjAsImlhdCI6MTQ4NjQxMjI2NSwiZXhwIjoxNDg2NTEyMzQ1fQ.vIRAUMytMiCQiTPOlY6vmoFrJqv7bv1fC-OCzJc9GpA")
	#     #socket.emitack("username","client1", ack)
	#     socket.onack("msg",onmessage)
	#     #Message=json.loads('{}')
	#     #Message["sender"]="client1"
	#     #Message["receiver"]="sachin"
	#     #Message["data"]="Hi I'm prince"
	#     #socket.emit("sendmsg",Message)

	def onconnect(self,socket):
	   logging.info("connected")

	def ondisconnect(self,socket):
	    logging.info("on disconnect got called")

	def onConnectError(self,socket, error):
	    logging.info("On connect error got called")

	def onSetAuthentication(self,socket, token): #called after token is set from server side
	    logging.info("Token received " + token)
	    socket.setAuthtoken(token)

	def onAuthentication(self,socket, isauthenticated):
	    logging.info("Authenticated is " + str(isauthenticated))
	    time.sleep(1)
	    socket.onack("msg",onmessage)

#################################################################################

	def sync_event(self):
		while(self.sync_thread_flag == 1):
			if(self.internet_on() == True):	#internet on
				self.log_count = 0
				socket = Socketcluster.socket("ws://localhost:8000/socketcluster/")
				socket.setBasicListener(self.onconnect, self.ondisconnect, self.onConnectError)
				socket.setAuthenticationListener(self.onSetAuthentication, self.onAuthentication)
				socket.setreconnection(False)
				socket.connect()
				while(True):
					if(self.internet_on() == False):
						break
    		else:
    			socket.disconnect()
    			self.send_offline_logs_flag = 0
			

if(internet_on() == True):
	print("Internet on")
else:
	print("Internet OFF")