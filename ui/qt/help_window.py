# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/qt/help_window.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Help_Window(object):
    def setupUi(self, Help_Window):
        Help_Window.setObjectName("Help_Window")
        Help_Window.resize(481, 252)
        self.frame = QtWidgets.QFrame(Help_Window)
        self.frame.setGeometry(QtCore.QRect(-10, 0, 161, 301))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.tips_button = QtWidgets.QPushButton(self.frame)
        self.tips_button.setGeometry(QtCore.QRect(20, 50, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.tips_button.setFont(font)
        self.tips_button.setStyleSheet("QPushButton\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"}")
        self.tips_button.setObjectName("tips_button")
        self.about_button = QtWidgets.QPushButton(self.frame)
        self.about_button.setGeometry(QtCore.QRect(20, 90, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.about_button.setFont(font)
        self.about_button.setStyleSheet("QPushButton\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"}")
        self.about_button.setObjectName("about_button")
        self.shortcut_button = QtWidgets.QPushButton(self.frame)
        self.shortcut_button.setGeometry(QtCore.QRect(20, 10, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.shortcut_button.setFont(font)
        self.shortcut_button.setStyleSheet("QPushButton\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"}")
        self.shortcut_button.setObjectName("shortcut_button")
        self.about_edit = QtWidgets.QTextEdit(Help_Window)
        self.about_edit.setGeometry(QtCore.QRect(160, 10, 311, 231))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.about_edit.setFont(font)
        self.about_edit.setStyleSheet("QTextEdit\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"}")
        self.about_edit.setReadOnly(True)
        self.about_edit.setObjectName("about_edit")
        self.tips_edit = QtWidgets.QTextEdit(Help_Window)
        self.tips_edit.setGeometry(QtCore.QRect(160, 10, 311, 231))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.tips_edit.setFont(font)
        self.tips_edit.setReadOnly(True)
        self.tips_edit.setObjectName("tips_edit")
        self.shortcut_edit = QtWidgets.QTextEdit(Help_Window)
        self.shortcut_edit.setGeometry(QtCore.QRect(160, 10, 311, 231))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.shortcut_edit.setFont(font)
        self.shortcut_edit.setReadOnly(True)
        self.shortcut_edit.setObjectName("shortcut_edit")

        self.retranslateUi(Help_Window)
        QtCore.QMetaObject.connectSlotsByName(Help_Window)

    def retranslateUi(self, Help_Window):
        _translate = QtCore.QCoreApplication.translate
        Help_Window.setWindowTitle(_translate("Help_Window", "HELP"))
        self.tips_button.setText(_translate("Help_Window", "TIPS"))
        self.about_button.setText(_translate("Help_Window", "ABOUT"))
        self.shortcut_button.setText(_translate("Help_Window", "SHORTCUTS"))
        self.about_edit.setHtml(_translate("Help_Window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Roboto\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Notelet lets you add notes corresponding to current active window. You can also synchronize notes across multiple machines.</span></p></body></html>"))
        self.tips_edit.setHtml(_translate("Help_Window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Roboto\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To be updated</p></body></html>"))
        self.shortcut_edit.setHtml(_translate("Help_Window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Roboto\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"4\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:12pt; font-weight:600;\"> PRESS</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:12pt; font-weight:600;\"> TO </span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:12pt;\"> CTRL + B </span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:12pt;\"> BOLD </span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:12pt;\"> CTRL + I </span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:12pt;\"> ITALIC </span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:12pt;\"> CTRL + U </span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:12pt;\"> UNDERLINE </span></p></td></tr></table></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Help_Window = QtWidgets.QWidget()
    ui = Ui_Help_Window()
    ui.setupUi(Help_Window)
    Help_Window.show()
    sys.exit(app.exec_())

