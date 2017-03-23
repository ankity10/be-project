# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reminder_msg_window.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Rem_MSG_Window(object):
    def setupUi(self, Rem_MSG_Window):
        Rem_MSG_Window.setObjectName("Rem_MSG_Window")
        Rem_MSG_Window.resize(326, 103)
        Rem_MSG_Window.setStyleSheet("QWidget\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"    background-color: rgb(255, 255, 255);\n"
"}")
        self.reminder_msg_edit = QtWidgets.QLineEdit(Rem_MSG_Window)
        self.reminder_msg_edit.setEnabled(True)
        self.reminder_msg_edit.setGeometry(QtCore.QRect(10, 10, 301, 41))
        self.reminder_msg_edit.setStyleSheet("QLineEdit\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"text-align : center;\n"
"\n"
"}")
        self.reminder_msg_edit.setFrame(False)
        self.reminder_msg_edit.setReadOnly(True)
        self.reminder_msg_edit.setObjectName("reminder_msg_edit")
        self.dismiss_button = QtWidgets.QPushButton(Rem_MSG_Window)
        self.dismiss_button.setGeometry(QtCore.QRect(20, 60, 131, 27))
        self.dismiss_button.setStyleSheet("QPushButton\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"    border-style : solid;\n"
"    border-radius : 10px;\n"
"border-width : 1px;\n"
"border-color : rgb(85, 170, 255);\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.dismiss_button.setObjectName("dismiss_button")
        self.snooze_button = QtWidgets.QPushButton(Rem_MSG_Window)
        self.snooze_button.setGeometry(QtCore.QRect(180, 60, 121, 27))
        self.snooze_button.setStyleSheet("QPushButton\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"    border-style : solid;\n"
"    border-radius : 10px;\n"
"border-width : 1px;\n"
"border-color : rgb(85,170,255);\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.snooze_button.setObjectName("snooze_button")

        self.retranslateUi(Rem_MSG_Window)
        QtCore.QMetaObject.connectSlotsByName(Rem_MSG_Window)

    def retranslateUi(self, Rem_MSG_Window):
        _translate = QtCore.QCoreApplication.translate
        Rem_MSG_Window.setWindowTitle(_translate("Rem_MSG_Window", "Form"))
        self.reminder_msg_edit.setText(_translate("Rem_MSG_Window", "                                    Its Time"))
        self.dismiss_button.setText(_translate("Rem_MSG_Window", "DISMISS"))
        self.snooze_button.setText(_translate("Rem_MSG_Window", "SNOOZE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Rem_MSG_Window = QtWidgets.QWidget()
    ui = Ui_Rem_MSG_Window()
    ui.setupUi(Rem_MSG_Window)
    Rem_MSG_Window.show()
    sys.exit(app.exec_())

