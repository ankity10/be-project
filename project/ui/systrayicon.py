import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView 
import time
from threading import Thread

    
class TrayIcon(QSystemTrayIcon):
    def __init__(self):
        QSystemTrayIcon.__init__(self)
        self.setIcon(QIcon('notes.png'))
        self.activated.connect(self.trayIconActivated)
        self.createIconMenu()
        self.show()

    def createIconMenu(self):
        self.trayIconMenu = QMenu()
        shownote = QAction('Note',self)
        shownote.triggered.connect(self.showtext)
        self.trayIconMenu.addAction(shownote)
        self.trayIconMenu.addSeparator()
        exitaction = QAction('Exit',self)
        exitaction.triggered.connect(self.exitapp)
        self.trayIconMenu.addAction(exitaction)
        self.setContextMenu(self.trayIconMenu)

    def exitapp(self):
        self.w.close()
        sys.exit(0)

    def showtext(self):
        self.w = MainWindow(self.geometry().topRight())
        
    def trayIconActivated(self,reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.showtext()

    def savenote(self):
        with open('note.txt','wt') as txt:
            print(self.edit.toHtml())
            txt.write(self.edit.toHtml())

    

class MainWindow(QMainWindow):
    def __init__(self, position):
        self.position = position
        self.thread_flag = 1
        super(MainWindow, self).__init__()
        self.setWindowTitle("Lazynote")
        widget = QWidget()
        self.layout = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.browser = QWebEngineView() 
        folder_path = os.path.abspath('./')
        abs_path = "file://" + folder_path + '/firepad/examples/richtext-simple.html'
        self.browser.load(QUrl(abs_path))
        self.setCentralWidget(self.browser)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setPosition()
        self.show()
        self.thread = Thread(target = self.return_html, args = (self.browser, ))
        self.thread_flag = 1
        self.thread.start()

    def setPosition(self):
        x = self.position.x() - self.width()/2;
        y = self.position.y()
        if y > 0:
            y = y - self.height()/2
        self.setGeometry(x,y,self.width()/2,self.height()/2)

    def return_html(self,browser):
        while(self.thread_flag == 1):
            x = browser.page().runJavaScript(str("firepad.getHtml()"),self.print_html)
            time.sleep(2)
    def print_html(self,y):
        print(y)

    def closeEvent(self,event):
        self.thread_flag = 0

if __name__ == '__main__':
    app=QApplication(sys.argv) 
    app.setQuitOnLastWindowClosed(False)
    trayicon=TrayIcon()
    app.exec_()

