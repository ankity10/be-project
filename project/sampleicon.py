import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TrayIcon(QSystemTrayIcon):
    def __init__(self):
        QSystemTrayIcon.__init__(self)
        self.setIcon(QIcon('graphics/notes.png'))
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
        sys.exit(0)

    def showtext(self):
        self.w = QMainWindow()
        self.w.setWindowTitle("Lazynote")
        widget = QWidget()
        self.layout = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.edit = QTextEdit()
        self.edit.currentCharFormatChanged.connect(self.currentformat)
        with open('note.txt','rt') as txt:
            self.edit.setText(txt.read())
        self.button = QPushButton('Save')
        self.layout.addWidget(self.edit)
        self.vbox.addLayout(self.layout)
        self.button.setFixedSize(100,25)
        self.vbox.addWidget(self.button)
        self.button.clicked.connect(self.savenote)
        widget.setLayout(self.vbox)
        self.w.setCentralWidget(widget)
        self.w.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setPosition()
        self.createmenu()
        self.w.show()

    def setPosition(self):
        pos = self.geometry().topRight()
        position = QDesktopWidget().screenGeometry().topRight()
        x = pos.x()
        print(x)
        if x < 0:
            x = position.x()
        x = x - self.w.width()/2
        y = pos.y()
        if(pos.y() > 0):
            y = y - self.w.height()/2
        self.w.setGeometry(x,y,self.w.width()/2,self.w.height()/2)

    def trayIconActivated(self,reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.showtext()

    def savenote(self):
        with open('note.txt','wt') as txt:
            txt.write(self.edit.toHtml())

    def createmenu(self):
        self.formatbar = self.w.addToolBar("Format")
        self.addBold()
        self.addItalic()
        self.addUnderline()
        self.addListStyle()

    def addBold(self):
        self.bold = QAction('B',self,checkable=True)
        self.bold.setShortcut("Ctrl+B")
        self.bold.triggered.connect(self.boldtext)
        boldfont = QFont()
        boldfont.setBold(True)
        self.bold.setFont(boldfont)
        self.formatbar.addAction(self.bold)

    def addItalic(self):
        self.italic = QAction('i',self,checkable=True)
        self.italic.setShortcut("Ctrl+I")
        self.italic.triggered.connect(self.italictext)
        italicfont = QFont()
        italicfont.setItalic(True)
        self.italic.setFont(italicfont)
        self.formatbar.addAction(self.italic)

    def addUnderline(self):
        self.underline = QAction('U',self,checkable=True)
        self.underline.setShortcut("Ctrl+U")
        self.underline.triggered.connect(self.underlinetext)
        ulfont = QFont()
        ulfont.setUnderline(True)
        self.underline.setFont(ulfont)
        self.formatbar.addAction(self.underline)

    def addListStyle(self):
        self.liststyle = QComboBox()
        self.formatbar.addWidget(self.liststyle)
        

    def boldtext(self):
        if self.edit.fontWeight() == QFont.Bold:

            self.edit.setFontWeight(QFont.Normal)

        else:

            self.edit.setFontWeight(QFont.Bold)

    def italictext(self):
        state = self.edit.fontItalic()
        self.edit.setFontItalic(not state)

    def underlinetext(self):
        state = self.edit.fontUnderline()
        self.edit.setFontUnderline(not state)

    def currentformat(self, format):
        self.currentfont(format.font())

    def currentfont(self, font):
        self.bold.setChecked(font.bold())
        self.italic.setChecked(font.italic())
        self.underline.setChecked(font.underline())

if __name__ == '__main__':
    app=QApplication(sys.argv) 
    app.setQuitOnLastWindowClosed(False)
    trayicon=TrayIcon()
    app.exec_()

