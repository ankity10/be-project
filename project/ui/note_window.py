#!/usr/bin/env python3
# vim:fileencoding=utf-8

from PyQt5.Qt import *
import os

class WebPage(QWebEnginePage):

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            print('{}: {}, {}'.format(source_id, linenumber, msg))
        except OSError:
            pass


class NoteWindow(QWebEngineView):

    def __init__(self):
        super().__init__()
        file_path = '/firepad/examples/richtext-simple.html'
        folder_path = os.path.abspath('./')
        self.abs_path = "file://" + folder_path + file_path
        self.show()

app = QApplication([])
default_text = "sdfsdf"
note_window = NoteWindow()
page = WebPage()
note_window.setPage(page)

if len(default_text):
    note_window.page().runJavaScript(str("window.onload = function() { init();firepad.setHtml('" + default_text + "')}"))

note_window.load(QUrl(note_window.abs_path))
app.exec_()