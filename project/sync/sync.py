import urllib.error
import threading
import asyncio
import websockets

from storage.storage2 import Local_Log
from urllib.request import urlopen

class sync:

	def __init__(self, main_app):
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

	async def retrieve_online_logs(self,websocket):
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
						self.main_app.storage.insert_note()


	async def send_offline_logs(self,websocket):
		log_collection = self.main_app.storage.log_collection.find({})
		for log in log_collection:
			await websocket.send(log)		

	def internet_on():
	    for timeout in [1,5,10,15]:
	        try:
	            response=urlopen('http://google.com',timeout=timeout)
	            return True
	        except urllib.error.URLError as err: pass
	    return False

	def sync_event(self):
		while(self.sync_thread_flag == 1):
			if(self.internet_on() == True):	#internet on
				ws = websocket.WebSocket()
				ws.connect('ws://localhost:8765')
				while(True):
					if(self.internet_on() == False):
						break
					else:
						self.retrieve_online_logs(ws)
						self.send_offline_logs(ws)
				
			

if(internet_on() == True):
	print("Internet on")
else:
	print("Internet OFF")