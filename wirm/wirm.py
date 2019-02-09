#!/usr/bin/env python3
"""
Execution Steps for python3:

1. Install xlib for python:
	i.	run: "sudo pip3 install python-xlib"

2. Execute program using "python3 wirm.py"
"""
import os
import threading
import time
import Xlib.display
import Xlib.threaded
from Xlib import error

global APP_NAME
APP_NAME = "LazyNotes"


class WIRM:
    def active_window_thread(self):
        self.active_window_thread_flag = 1
        t = threading.Thread(target=self.window_change_event)
        t.start()

    def __init__(self, main_app):
        self.main_app = main_app
        self.display = Xlib.display.Display(str(os.environ["DISPLAY"]))
        self.root = self.display.screen().root
        self.active = self.display.screen().root
        self.thread_toggle = 0
        self.active_window_id = 0
        self.prev_active_window_id = 1
        self.active_window_thread_flag = 0
        self.prev_active_window_title = ""
        self.active_window_title = ""
        self.prev_active_window_name = ""
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

    def window_change_event(self):
        while (self.active_window_thread_flag == 1):
            atom = self.display.intern_atom('_NET_ACTIVE_WINDOW', True)
            temp_active_window_id = (self.root.get_full_property(atom, Xlib.X.AnyPropertyType).value[0])
            active = self.display.create_resource_object('window', temp_active_window_id)
            atom = self.display.intern_atom('_NET_WM_NAME', True)
            try:
                # print(".")
                w = (active).get_full_property(atom, Xlib.X.AnyPropertyType).value
            except:
                # print("*")
                continue
            if (w.decode("utf8") != self.active_window_title):
                print("----------------------------------------------------")
                self.win = w.decode("utf8")
                print('!!!Window changed!!!!')
                self.prev_active_window_title = self.active_window_title
                self.active_window_title = w.decode("utf8")
                print("************Previous window title :", self.prev_active_window_title)
                print("************Current window title :", self.active_window_title)
                self.prev_active_window_id = self.active_window_id
                self.active_window_id = temp_active_window_id
                self.get_active_window_name()
                self.main_app.show_note()
            time.sleep(0.1)
        # print(".")
        print("main_app thread stopped!!")

    def default_active_window_event(self):
        global APP_NAME
        self.active_window_id = self.get_active_window_id()
        # print("*******"+str(self.active_window_id)+"*********")
        self.root.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
        while (self.active_window_thread_flag == 1):
            atom = self.display.intern_atom('_NET_ACTIVE_WINDOW', True)
            try:
                temp_active_window_id = (self.root.get_full_property(atom, Xlib.X.AnyPropertyType).value[0])
            except:
                continue
            active = self.display.create_resource_object('window', temp_active_window_id)
            atom = self.display.intern_atom('_NET_WM_NAME', True)
            try:
                w = (active).get_full_property(atom, Xlib.X.AnyPropertyType).value
                # print("-------------"+str(w.decode("utf8"))+"------------")
                if (w.decode("utf8") == APP_NAME or w.decode("utf8") == "None"):
                    print("-------------APP ACTIVE------------")
                    continue
            except:
                continue
            if (w.decode("utf8") != self.active_window_title):
                self.thread_scheduler = not self.thread_scheduler  # to ensure this thread executes before main_app thread
                print('Window changed!')
                self.prev_active_window_title = self.active_window_title
                self.active_window_title = w.decode("utf8")
                self.active_window_id = temp_active_window_id
                print("*******" + str(self.active_window_id) + "*********")
            time.sleep(0.1)
        self.thread_scheduler = -1  # For Thread Stop
        print("thread stopped!!")

    # Retrieving active window id
    def get_active_window_id(self):
        atom = self.display.intern_atom('_NET_ACTIVE_WINDOW', True)
        # print("#################"+str(atom)+"##################")
        try:
            active_window_id = (self.root.get_full_property(atom, Xlib.X.AnyPropertyType).value[0])
            if (self.is_ewmh_supported(atom, self.root) == False):
                print("EWMH is not supported by your window manager!!")
                return None
        except:
            return None
        return (active_window_id)

    # Retrieving active window pid
    def get_active_window_pid(self):
        atom = self.display.intern_atom('_NET_WM_PID')
        try:
            self.window_pid = self.active.get_full_property(atom, Xlib.X.AnyPropertyType).value[0]
        except:
            print("---_______else")
            return (self.window_pid)
        return (self.window_pid)

    # Retrieving active window process name from process id
    def get_process_name(self, window_pid):
        pid_path = os.path.join('/proc', str(window_pid))
        if os.path.exists(pid_path):
            with open(os.path.join(pid_path, 'comm')) as f:
                process_name = f.read().rstrip('\n')  # Read and Remove \n
                if process_name in ["chrome", "firefox", "chromium-browse"]:
                    process_name = "BROWSER"
                return (process_name)
        else:
            print("No such PID in Running processes!!")

    # Retrieving active window title
    def get_active_window_title(self, session_num=1,
                                active_window_id=int):  # session_num = 0 if note option is clicked else 1
        # print("\nSession Number" + str(session_num))
        active_window_id = self.active_window_id
        if (str(os.environ["DESKTOP_SESSION"]) == "xfce" and session_num == 0):
            print("Session Number 0")
            self.active_window_id = self.prev_active_window_id
            active_window_id = self.active_window_id
        elif (str(os.environ["DESKTOP_SESSION"]) == "xubuntu" and session_num == 0):
            self.active_window_id = self.prev_active_window_id
            active_window_id = self.active_window_id
        else:
            self.active_window_id = self.get_active_window_id()
            active_window_id = self.active_window_id
        self.thread_toggle = not self.thread_toggle
        # print("ACTIVE EINDOW ID = "+str(active_window_id))
        self.active = self.display.create_resource_object('window', active_window_id)
        # print("-----------------"+str(self.active))
        atom = self.display.intern_atom('_NET_WM_NAME', True)
        if (self.is_ewmh_supported(atom, self.root) == False):
            print("EWMH is not supported by your window manager!!")
            return None  # return
        ec = error.CatchError(error.BadWindow)
        try:
            w = (self.active).get_full_property(atom, Xlib.X.AnyPropertyType).value
        except:
            print("************************Bad Window")
            return (self.active_window_title)
        try:
            # self.prev_active_window_title = self.active_window_title
            self.active_window_title = w.decode("utf8")
            print("Previous window title :", self.prev_active_window_title)
            print("Current window title :", self.active_window_title)
        except:
            return (self.active_window_title)
        return (self.active_window_title)

    def get_active_window_name(self, session_num=1):
        while (self.active_window_thread_flag == 0):
            continue
        if (str(os.environ["DESKTOP_SESSION"]) == "xfce" and session_num == 0):
            self.active_window_id = self.prev_active_window_id
            print("process name")
        elif (str(os.environ["DESKTOP_SESSION"]) == "xubuntu" and session_num == 0):
            self.active_window_id = self.prev_active_window_id
        else:
            self.active_window_id = self.get_active_window_id()
        print("ACTIVE EINDOW ID = " + str(self.active_window_id))
        self.active = self.display.create_resource_object('window', self.active_window_id)
        window_pid = self.get_active_window_pid()
        if (self.get_process_name(window_pid) != self.active_window_name):
            self.prev_active_window_name = self.active_window_name
            self.active_window_name = self.get_process_name(window_pid)
            self.thread_toggle = not self.thread_toggle
        print("Previous process name :", self.prev_active_window_name)
        print("Current process name :", self.active_window_name)
        return (self.active_window_name)


def main():
    w = WIRM()
    while True:
        title = w.get_active_window_title()
        print(title)
        time.sleep(1)


if __name__ == '__main__':
    main()
