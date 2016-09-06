"""
Execution Steps for python3:

1. Install xlib for python:
	i.	run: "sudo pip3 install python-xlib"

2. Execute program using "python3 wirm.py"
"""

import Xlib.display
import subprocess
import time

def is_ewmh_supported(display, atom_request, window):
	atom_supported = display.intern_atom('_NET_SUPPORTED')
	atom_supported_list = window.get_full_property(atom_supported, Xlib.X.AnyPropertyType).value
	for atom in atom_supported_list:
		if (atom == atom_request):
			return True
	return False


while(1):
	#Retrieving active window id
	display = Xlib.display.Display(':0')
	root = display.screen().root
	atom = display.intern_atom('_NET_ACTIVE_WINDOW',True)
	if (is_ewmh_supported(display,atom,root) == False):
		print ("EWMH is not supported by your window manager!!")
		break				#return
	active_window_id = root.get_full_property(atom, Xlib.X.AnyPropertyType).value[0]
	#print (active_window_id)

	#Retrieving active window title
	active = display.create_resource_object('window', active_window_id) 
	atom = display.intern_atom('_NET_WM_NAME',True)
	if (is_ewmh_supported(display,atom,root) == False):
		print ("EWMH is not supported by your window manager!!")
		break				#return
	w = active.get_full_property(atom, Xlib.X.AnyPropertyType).value
	window_name = w.decode("utf8")
	print (w)
	
	#Retrieving active window pid
	atom = display.intern_atom('_NET_WM_PID')
	window_pid = active.get_full_property(atom, Xlib.X.AnyPropertyType).value[0] 
	#print (window_pid)
	
	#Retrieving active window process name
	process = subprocess.Popen(("ps -p " + str(window_pid) + " -o comm="),shell=True, stdout=subprocess.PIPE)
	process_name = process.communicate()[0].decode("utf8").split('\n')[0]	#To remove \n
	print (process_name)
	
	time.sleep(1)