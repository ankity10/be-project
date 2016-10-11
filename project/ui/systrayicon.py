import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QSystemTrayIcon, 
                                QApplication, 
                                QMenu, 
                                QAction, 
                                QWidget, 
                                QTextEdit, 
                                QVBoxLayout, 
                                QPushButton)


class TrayIcon(QSystemTrayIcon):
    def __init__(self):
        QSystemTrayIcon.__init__(self)
        self.setIcon(QIcon('icon.png'))
        self.activated.connect(self.on_tray_activated)

        # setting up context menu
        self.trayIconMenu = QMenu()
        shownote = QAction('Note',self)
        shownote.triggered.connect(self.display_note)
        self.trayIconMenu.addAction(shownote)
        self.trayIconMenu.addSeparator()
        exitaction = QAction('Exit',self)
        exitaction.triggered.connect(self.exit)
        self.trayIconMenu.addAction(exitaction)
        self.setContextMenu(self.trayIconMenu)

        self.show()
        
    def on_tray_activated(self, reason):
        reason = str(reason)
        if reason == '3':
            self.display_note()
        elif reason == '1':
            pass
            # print("show menu")
    
    def display_note(self):
        self.w = QWidget()
        # self.w.setWindowTitle("Ankit")
        self.layout = QVBoxLayout()
        self.edit = QTextEdit()
        txt = open('note.txt')
        self.edit.append(txt.read())
        # self.edit.append(str(reason))
        txt.close()
        self.button = QPushButton('Save')
        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.save_note)
        self.w.setLayout(self.layout)
        self.w.setWindowFlags(Qt.WindowStaysOnTopHint)
        pos = self.geometry().topRight()
        x, y = pos.x() - self.w.width()/2 + 50, pos.y() - self.w.height() 
        self.w.move(x,y)
        self.w.show()

    def exit(self):
        sys.exit(0)

    def save_note(self):
        mytext = self.edit.toPlainText()
        with open('note.txt','w') as txt:
            txt.write(mytext)

if __name__ == '__main__':
    app=QApplication(sys.argv) 
    app.setQuitOnLastWindowClosed(False)
    trayicon=TrayIcon()
    sys.exit(app.exec_())
