#!/usr/bin/env python3
# vim:fileencoding=utf-8

from PyQt5.Qt import *
import os
import sys
import datetime
from storage.storage import db_api
from wirm.wirm import WIRM
global status 
global storage


class WebPage(QWebEnginePage):

    def __init__(self, status):
        super().__init__()
        self.status = status

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            hashed_key = sys.argv[1]
            process_name = sys.argv[2]
            window_title = sys.argv[3]
            time = datetime.datetime.now().time()
            current_time = time.isoformat()
            text = msg
            if self.status == "new":
                storage.insert(hashed_key, text, current_time, window_title, process_name)
                self.status = "old"
                print("new note inserted")
            elif self.status == "old":
                storage.update(hashed_key, text, current_time, window_title, process_name)
                print("note updated")
        except OSError:
            pass


class NoteWindow(QWebEngineView):

    def __init__(self):
        super().__init__()
        file_path = '/ui/examples/richtext-simple.html'
        folder_path = os.path.abspath('./')
        self.abs_path = "file://" + folder_path + file_path
        self.show()

app = QApplication([])
print(sys.argv)

hashed_key = sys.argv[1]
process_name = sys.argv[2]
window_title = sys.argv[3]
time = datetime.datetime.now().time()
current_time = time.isoformat()
storage = db_api()
note = storage.read_note_from_db(hashed_key)

if note:
    default_text = note.note_attr_obj.note_info
    status = "old"
else:
    default_text = "empty" 
    status = "new"

note_window = NoteWindow()
# note_window.setWindowFlags(Qt.WindowStaysOnTopHint)
page = WebPage(status)
note_window.setPage(page)
note_window.page().runJavaScript(str("window.onload = function() { init();firepad.setHtml('" + default_text + "')}"))
note_window.load(QUrl(note_window.abs_path))
app.exec_()