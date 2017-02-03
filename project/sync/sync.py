import urllib.error
import threading

from urllib.request import urlopen

class sync:

	def __init__(self, main_app):
		self.main_app = main_app
		self.sync_thread_flag = 1
		t = threading.Thread(target=self.sync_event)
		t.start()

	def client_online(self):
			

	def internet_on():
	    for timeout in [1,5,10,15]:
	        try:
	            response=urlopen('http://google.com',timeout=timeout)
	            return True
	        except urllib.error.URLError as err: pass
	    return False

	def sync_event(self):
		while(self.sync_thread_flag == 1):
			if(self.internet_on == True):	#internet on
				self.client_online()


if(internet_on() == True):
	print("Internet on")
else:
	print("Internet OFF")