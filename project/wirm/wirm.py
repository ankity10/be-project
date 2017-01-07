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
from Xlib import error
import subprocess
import os
import time

APP_NAME = "LazyNotes"

class WIRM:
	def active_window_thread(self):
		self.active_window_thread_flag = 1
		if(str(os.environ["DESKTOP_SESSION"]) == "ubuntu" or str(os.environ["DESKTOP_SESSION"]) == "gnome"):
			return
		elif(str(os.environ["DESKTOP_SESSION"]) == "xfce" or str(os.environ["DESKTOP_SESSION"]) == "xubuntu"):
			t = threading.Thread(target=self.xfce_active_window_event)
			t.start()
		else:		
			t = threading.Thread(target=self.default_active_window_event)
			t.start()

		
	def __init__(self):
		self.display = Xlib.display.Display(str(os.environ["DISPLAY"]))
		self.root = self.display.screen().root
		self.active = self.display.screen().root
		self.active_window_id = 0
		self.prev_active_window_id = 1
		self.active_window_thread_flag = 0 
		self.active_window_title = ""
		self.active_window_name = ""
		self.window_pid = "1"
		self.thread_scheduler = 0
		self.active_window_thread()

	def is_ewmh_supported(self, atom_request, window):
		atoms_supported = self.display.intern_atom('_NET_SUPPORTED')
		atoms_supported_list = window.get_full_property(atoms_supported, Xlib.X.AnyPropertyType).value
		for atom in atoms_supported_list:
			if (atom == atom_request):
				return True
		return False

	def xfce_active_window_event(self):
		print("!!!!!!!!!!!!xfce event!!!!!!!!!!")
		self.active_window_id = self.get_active_window_id()
		print("*******"+str(self.active_window_id)+"*********")
		self.root.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
		while (self.active_window_thread_flag == 1):
			atom = self.display.intern_atom('_NET_ACTIVE_WINDOW',True)
			try:
				temp_active_window_id = (self.root.get_full_property(atom, Xlib.X.AnyPropertyType).value[0])
			except:
				continue
			active = self.display.create_resource_object('window', temp_active_window_id) 
			atom = self.display.intern_atom('_NET_WM_NAME',True)
			try:
				w = (active).get_full_property(atom, Xlib.X.AnyPropertyType).value
				#print("-------------"+str(w.decode("utf8"))+"------------")
				if(w.decode("utf8") == APP_NAME or w.decode("utf8") == "None"):
					print("-------------APP ACTIVE------------")
					continue
			except:
				continue
			if(w.decode("utf8") != self.active_window_title):
				self.thread_scheduler = not self.thread_scheduler	#to ensure this thread executes before main_app thread
				print ('Window changed!')
				self.active_window_title = w.decode("utf8")
				if(self.active_window_id == temp_active_window_id):
					continue
				self.prev_active_window_id = self.active_window_id
				self.active_window_id = temp_active_window_id
				print("previous :" + str(self.prev_active_window_id))
				print("next :" + str(self.active_window_id))
				print("*******"+str(self.active_window_id)+"*********")
			time.sleep(0.1)
		self.thread_scheduler = -1	#For Thread Stop
		print("wirm thread stopped!!")


	def default_active_window_event(self):
		global APP_NAME
		self.active_window_id = self.get_active_window_id()
		# print("*******"+str(self.active_window_id)+"*********")
		self.root.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
		while (self.active_window_thread_flag == 1):
			atom = self.display.intern_atom('_NET_ACTIVE_WINDOW',True)
			try:
				temp_active_window_id = (self.root.get_full_property(atom, Xlib.X.AnyPropertyType).value[0])
			except:
				continue
			active = self.display.create_resource_object('window', temp_active_window_id) 
			atom = self.display.intern_atom('_NET_WM_NAME',True)
			try:
				w = (active).get_full_property(atom, Xlib.X.AnyPropertyType).value
				#print("-------------"+str(w.decode("utf8"))+"------------")
				if(w.decode("utf8") == APP_NAME or w.decode("utf8") == "None"):
					print("-------------APP ACTIVE------------")
					continue
			except:
				continue
			if(w.decode("utf8") != self.active_window_title):
				self.thread_scheduler = not self.thread_scheduler	#to ensure this thread executes before main_app thread
				print ('Window changed!')
				self.active_window_title = w.decode("utf8")
				self.active_window_id = temp_active_window_id
				print("*******"+str(self.active_window_id)+"*********")
			time.sleep(0.1)
		self.thread_scheduler = -1	#For Thread Stop
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
		try:
			self.window_pid = self.active.get_full_property(atom, Xlib.X.AnyPropertyType).value[0] 
		except:
			print("---_______else")
			return (self.window_pid)	
		return (self.window_pid)
		
	#Retrieving active window process name from process id
	def get_process_name(self, window_pid):
		pid_path = os.path.join('/proc', str(window_pid))
		if os.path.exists(pid_path):
		    with open(os.path.join(pid_path, 'comm')) as f:
		        process_name = f.read().rstrip('\n') #Read and Remove \n
		        return (process_name)
		else:
			print("No such PID in Running processes!!")

	#Retrieving active window title
	def get_active_window_title(self,session_num = 1,active_window_id = int):	#session_num = 0 if note option is clicked else 1
		active_window_id = self.active_window_id
		if(str(os.environ["DESKTOP_SESSION"]) == "xfce" and session_num == 0):
			self.active_window_id = self.prev_active_window_id
			active_window_id = self.active_window_id
		elif(str(os.environ["DESKTOP_SESSION"]) == "xubuntu" and session_num == 0):
			self.active_window_id = self.prev_active_window_id
			active_window_id = self.active_window_id
		else:
			self.active_window_id = self.get_active_window_id()
			active_window_id = self.active_window_id
		self.active = self.display.create_resource_object('window', active_window_id) 
		#print("-----------------"+str(self.active))
		atom = self.display.intern_atom('_NET_WM_NAME',True)
		if (self.is_ewmh_supported(atom,self.root) == False):
			print ("EWMH is not supported by your window manager!!")
			return None				#return
		ec = error.CatchError(error.BadWindow)
		try:
			w = (self.active).get_full_property(atom, Xlib.X.AnyPropertyType).value
		except:
			print ("************************Bad Window")
			return (self.active_window_title)
		try:
			self.active_window_title = w.decode("utf8")
		except:
			return (self.active_window_title)	
		return (self.active_window_title)

	def get_active_window_name(self, session_num = 1):
		while(self.active_window_thread_flag == 0):
			continue
		if(str(os.environ["DESKTOP_SESSION"]) == "xfce" and session_num == 0):
			self.active_window_id = self.prev_active_window_id
			print("process name")
		if(str(os.environ["DESKTOP_SESSION"]) == "xubuntu" and session_num == 0):
			self.active_window_id = self.prev_active_window_id
		else:
			self.active_window_id = self.get_active_window_id()
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