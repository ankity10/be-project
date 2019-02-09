"""
Execution Steps for python3:

1. Install xlib for python:
	i.	run: "sudo pip3 install python-xlib"

2. Execute program using "python3 wirm.py"
"""

import Xlib.display
import subprocess
import time


class wirm:
    def __init__(self):
        self.display = Xlib.display.Display(':1')
        self.root = self.display.screen().root
        self.active = self.display.screen().root
        self.active_window_id = int
        self.active_window_title = ""
        self.active_window_name = ""

    def is_ewmh_supported(self, atom_request, window):
        atoms_supported = self.display.intern_atom('_NET_SUPPORTED')
        atoms_supported_list = window.get_full_property(atoms_supported, Xlib.X.AnyPropertyType).value
        for atom in atoms_supported_list:
            if (atom == atom_request):
                return True
        return False

    # Retrieving active window id
    def get_active_window_id(self):
        atom = self.display.intern_atom('_NET_ACTIVE_WINDOW', True)
        if (self.is_ewmh_supported(atom, self.root) == False):
            print("EWMH is not supported by your window manager!!")
            return None  # return
        self.active_window_id = int(self.root.get_full_property(atom, Xlib.X.AnyPropertyType).value[0])
        return (self.active_window_id)

    # Retrieving active window pid
    def get_active_window_pid(self):
        atom = self.display.intern_atom('_NET_WM_PID')
        window_pid = self.active.get_full_property(atom, Xlib.X.AnyPropertyType).value[0]
        return (window_pid)

    # Retrieving active window process name from process id
    def get_process_name(self, window_pid):
        process = subprocess.Popen(("ps -p " + str(window_pid) + " -o comm="), shell=True, stdout=subprocess.PIPE)
        get_process_name = process.communicate()[0].decode("utf8").split('\n')[0]  # To remove \n
        return (get_process_name)

    # Retrieving active window title
    def get_active_window_title(self):
        self.get_active_window_id()
        self.active = self.display.create_resource_object('window', self.active_window_id)
        atom = self.display.intern_atom('_NET_WM_NAME', True)
        if (self.is_ewmh_supported(atom, self.root) == False):
            print("EWMH is not supported by your window manager!!")
            return None  # return
        w = (self.active).get_full_property(atom, Xlib.X.AnyPropertyType).value
        self.active_window_title = w.decode("utf8")
        return (self.active_window_title)

    def get_active_window_name(self):
        self.get_active_window_id()
        self.active = self.display.create_resource_object('window', self.active_window_id)
        window_pid = self.get_active_window_pid()
        self.active_window_name = self.get_process_name(window_pid)
        return (self.active_window_name)


w = wirm()
while True:
    s = w.get_active_window_title()
    print(s)
    time.sleep(1)
