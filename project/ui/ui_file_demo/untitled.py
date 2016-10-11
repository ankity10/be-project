# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(262, 461)
        Form.setStyleSheet(_fromUtf8("QWidget {\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:0.994318, stop:0 rgba(255, 255, 255, 255), stop:0.25 rgba(232, 244, 63, 255), stop:0.595455 rgba(214, 229, 59, 255), stop:1 rgba(205, 220, 57, 255))\n"
"}\n"
""))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(20, 10, 31, 27))
        self.pushButton.setStyleSheet(_fromUtf8(""))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 10, 31, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 10, 51, 27))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(160, 10, 51, 27))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.toolButton = QtGui.QToolButton(Form)
        self.toolButton.setGeometry(QtCore.QRect(220, 10, 31, 27))
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(0, 40, 261, 421))
        self.textEdit.setStyleSheet(_fromUtf8("QTextEdit {\n"
"border: 0;\n"
"}"))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "B", None))
        self.pushButton_2.setText(_translate("Form", "I", None))
        self.pushButton_3.setText(_translate("Form", "uo list", None))
        self.pushButton_4.setText(_translate("Form", "o list", None))
        self.toolButton.setText(_translate("Form", "...", None))

