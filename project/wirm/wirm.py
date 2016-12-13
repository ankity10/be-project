#!/usr/bin/env python3
"""
Execution Steps for python3:

1. Install xlib for python:
	i.	run: "sudo pip3 install python-xlib"

2. Execute program using "python3 wirm.py"
"""
import threading
import Xlib.display
import Xlib.threaded
import subprocess
import os
import time

class WIRM:
	def active_window_thread(self):
		self.active_window_thread_flag = 1
		t = threading.Thread(target=self.active_window_event)
		t.start()

	def __init__(self):
		self.display = Xlib.display.Display(str(os.environ["DISPLAY"]))
		self.root = self.display.screen().root
		self.active = self.display.screen().root
		self.active_window_id = int
		self.active_window_thread_flag = 0 
		self.active_window_title = ""
		self.active_window_name = ""
		self.active_window_thread()

	def is_ewmh_supported(self,atom_request, window):
		atoms_supported = self.display.intern_atom('_NET_SUPPORTED')
		atoms_supported_list = window.get_full_property(atoms_supported, Xlib.X.AnyPropertyType).value
		for atom in atoms_supported_list:
			if (atom == atom_request):
				return True
		return False


	def active_window_event(self):
		self.active_window_id = self.get_active_window_id()
		print("*******"+str(self.active_window_id)+"*********")
		self.root.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
		while (self.active_window_thread_flag == 1):
			while self.display.pending_events():
				event = self.display.next_event()
				if type(event) == Xlib.protocol.event.PropertyNotify:
					atom_name = self.display.get_atom_name(event.atom)
					if (atom_name == '_NET_ACTIVE_WINDOW'):
						print ('Window changed!')
						temp_active_window_id = self.get_active_window_id()
						if(temp_active_window_id == 0):
							continue
						else:
							self.active_window_id = temp_active_window_id
						print("*******"+str(self.active_window_id)+"*********")

			time.sleep(0.1)
		print("thread stopped!!")


	#Retrieving active window id
	def get_active_window_id(self):
		atom = self.display.intern_atom('_NET_ACTIVE_WINDOW',True)
		if (self.is_ewmh_supported(atom,self.root) == False):
			print ("EWMH is not supported by your window manager!!")
			return None				#return
		print("#################"+str(atom)+"##################")
		active_window_id = (self.root.get_full_property(atom, Xlib.X.AnyPropertyType).value[0]) 
		return(active_window_id)
	
	#Retrieving active window pid
	def get_active_window_pid(self):
		atom = self.display.intern_atom('_NET_WM_PID')
		window_pid = self.active.get_full_property(atom, Xlib.X.AnyPropertyType).value[0] 
		return (window_pid)
		
	#Retrieving active window process name from process id
	def get_process_name(self,window_pid):
		process = subprocess.Popen(("ps -p " + str(window_pid) + " -o comm="),shell=True, stdout=subprocess.PIPE)
		get_process_name = process.communicate()[0].decode("utf8").split('\n')[0]	#To remove \n
		return (get_process_name)

	#Retrieving active window title
	def get_active_window_title(self):
		self.active = self.display.create_resource_object('window', self.active_window_id) 
		atom = self.display.intern_atom('_NET_WM_NAME',True)
		if (self.is_ewmh_supported(atom,self.root) == False):
			print ("EWMH is not supported by your window manager!!")
			return None				#return
		w = (self.active).get_full_property(atom, Xlib.X.AnyPropertyType).value
		self.active_window_title = w.decode("utf8")
		print(self.active_window_title)
		return (self.active_window_title)

	def get_active_window_name(self):
		self.active = self.display.create_resource_object('window', self.active_window_id)
		window_pid = self.get_active_window_pid()
		self.active_window_name = self.get_process_name(window_pid)
		return (self.active_window_name)

def main():
	w = WIRM()
	while True:
		title = w.get_active_window_title()
		print (title)
		time.sleep(1)
	
if __name__ == '__main__':
	main()