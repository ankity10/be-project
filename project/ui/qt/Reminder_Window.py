# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/qt/Reminder_Window.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Reminder_Window(object):
    def setupUi(self, Reminder_Window):
        Reminder_Window.setObjectName("Reminder_Window")
        Reminder_Window.resize(400, 498)
        Reminder_Window.setToolTip("")
        Reminder_Window.setStyleSheet("QWidget\n"
"{\n"
"    background-color: rgb(255, 255, 255);\n"
"    font: 11pt \"Roboto\";\n"
"}")
        self.less_options_button = QtWidgets.QCommandLinkButton(Reminder_Window)
        self.less_options_button.setGeometry(QtCore.QRect(150, 280, 111, 31))
        self.less_options_button.setStyleSheet("QCommandLinkButton\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"    text-decoration: underline;\n"
"    \n"
"    color: rgb(68, 137, 206);\n"
"    qproperty-icon : None\n"
"}")
        self.less_options_button.setObjectName("less_options_button")
        self.add_button = QtWidgets.QPushButton(Reminder_Window)
        self.add_button.setGeometry(QtCore.QRect(230, 240, 131, 41))
        self.add_button.setStyleSheet("QPushButton\n"
"{\n"
"color: #fff;\n"
"    font: 11pt \"Roboto\";\n"
"border-style: solid;\n"
"border-color: rgb(79, 159, 239);\n"
"border-width: 1px;\n"
"border-radius: 4px;\n"
"    \n"
"    background-color: rgb(79, 159, 239);\n"
"}")
        self.add_button.setFlat(False)
        self.add_button.setObjectName("add_button")
        self.cancel_button = QtWidgets.QPushButton(Reminder_Window)
        self.cancel_button.setGeometry(QtCore.QRect(40, 240, 131, 41))
        self.cancel_button.setStyleSheet("QPushButton\n"
"{\n"
"color:#fff;\n"
"    font: 11pt \"Roboto\";\n"
"border-style: solid;\n"
"border-color: rgb(212, 0, 0);\n"
"border-width: 1px;\n"
"border-radius: 4px;\n"
"    background-color: rgb(212, 0, 0);\n"
"}")
        self.cancel_button.setObjectName("cancel_button")
        self.label_2 = QtWidgets.QLabel(Reminder_Window)
        self.label_2.setGeometry(QtCore.QRect(230, 100, 68, 17))
        self.label_2.setStyleSheet("QLabel\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"}")
        self.label_2.setObjectName("label_2")
        self.repetition_label = QtWidgets.QLabel(Reminder_Window)
        self.repetition_label.setGeometry(QtCore.QRect(70, 180, 91, 31))
        self.repetition_label.setStyleSheet("QLabel\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"}")
        self.repetition_label.setObjectName("repetition_label")
        self.event_title_edit = QtWidgets.QLineEdit(Reminder_Window)
        self.event_title_edit.setGeometry(QtCore.QRect(20, 30, 361, 41))
        self.event_title_edit.setStyleSheet("QLineEdit\n"
"{\n"
"    font:  11pt \"Roboto\";\n"
"border-style: solid;\n"
"border-color: black;\n"
"border-width: 1px;\n"
"border-radius: 4px;\n"
"    background-color: rgb(255, 255, 255)\n"
"}")
        self.event_title_edit.setFrame(True)
        self.event_title_edit.setObjectName("event_title_edit")
        self.reminder_label = QtWidgets.QLabel(Reminder_Window)
        self.reminder_label.setGeometry(QtCore.QRect(70, 230, 81, 20))
        self.reminder_label.setStyleSheet("QLabel\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"}")
        self.reminder_label.setObjectName("reminder_label")
        self.target_date_edit = QtWidgets.QDateEdit(Reminder_Window)
        self.target_date_edit.setGeometry(QtCore.QRect(49, 120, 121, 31))
        self.target_date_edit.setStyleSheet("QDateEdit\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"}")
        self.target_date_edit.setFrame(False)
        self.target_date_edit.setCalendarPopup(True)
        self.target_date_edit.setObjectName("target_date_edit")
        self.target_time_edit = QtWidgets.QTimeEdit(Reminder_Window)
        self.target_time_edit.setGeometry(QtCore.QRect(230, 120, 118, 31))
        self.target_time_edit.setStyleSheet("QTimeEdit\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"}")
        self.target_time_edit.setFrame(True)
        self.target_time_edit.setObjectName("target_time_edit")
        self.repetition_options = QtWidgets.QComboBox(Reminder_Window)
        self.repetition_options.setGeometry(QtCore.QRect(190, 180, 141, 24))
        self.repetition_options.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        self.repetition_options.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.repetition_options.setFrame(False)
        self.repetition_options.setObjectName("repetition_options")
        self.repetition_options.addItem("")
        self.repetition_options.addItem("")
        self.repetition_options.addItem("")
        self.repetition_options.addItem("")
        self.more_options_button = QtWidgets.QCommandLinkButton(Reminder_Window)
        self.more_options_button.setGeometry(QtCore.QRect(140, 180, 121, 31))
        self.more_options_button.setStyleSheet("QCommandLinkButton\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"    text-decoration: underline;\n"
"    \n"
"    color: rgb(68, 137, 206);\n"
"    qproperty-icon : None\n"
"}")
        self.more_options_button.setObjectName("more_options_button")
        self.label = QtWidgets.QLabel(Reminder_Window)
        self.label.setGeometry(QtCore.QRect(50, 100, 68, 17))
        self.label.setStyleSheet("QLabel\n"
"{\n"
"    font: 11pt \"Roboto\";\n"
"}")
        self.label.setObjectName("label")
        self.reminder_options = QtWidgets.QComboBox(Reminder_Window)
        self.reminder_options.setGeometry(QtCore.QRect(190, 230, 141, 27))
        self.reminder_options.setFrame(False)
        self.reminder_options.setObjectName("reminder_options")
        self.reminder_options.addItem("")
        self.reminder_options.addItem("")
        self.reminder_options.addItem("")
        self.reminder_options.addItem("")
        self.reminder_options.addItem("")
        self.reminder_options.addItem("")

        self.retranslateUi(Reminder_Window)
        self.repetition_options.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Reminder_Window)

    def retranslateUi(self, Reminder_Window):
        _translate = QtCore.QCoreApplication.translate
        Reminder_Window.setWindowTitle(_translate("Reminder_Window", "Reminder"))
        self.less_options_button.setText(_translate("Reminder_Window", "Less Options?"))
        self.add_button.setText(_translate("Reminder_Window", "ADD"))
        self.cancel_button.setText(_translate("Reminder_Window", "CANCEL"))
        self.label_2.setText(_translate("Reminder_Window", "Time"))
        self.repetition_label.setText(_translate("Reminder_Window", "Repetition"))
        self.event_title_edit.setPlaceholderText(_translate("Reminder_Window", "                               Remind me about....."))
        self.reminder_label.setText(_translate("Reminder_Window", "Remind Me"))
        self.repetition_options.setItemText(0, _translate("Reminder_Window", "One time event"))
        self.repetition_options.setItemText(1, _translate("Reminder_Window", "Daily"))
        self.repetition_options.setItemText(2, _translate("Reminder_Window", "Weekly"))
        self.repetition_options.setItemText(3, _translate("Reminder_Window", "Monthly"))
        self.more_options_button.setText(_translate("Reminder_Window", "More Options?"))
        self.label.setText(_translate("Reminder_Window", "Date"))
        self.reminder_options.setItemText(0, _translate("Reminder_Window", "On time"))
        self.reminder_options.setItemText(1, _translate("Reminder_Window", "5 mins early"))
        self.reminder_options.setItemText(2, _translate("Reminder_Window", "10 mins early"))
        self.reminder_options.setItemText(3, _translate("Reminder_Window", "1 hour early"))
        self.reminder_options.setItemText(4, _translate("Reminder_Window", "2 hours early"))
        self.reminder_options.setItemText(5, _translate("Reminder_Window", "1 day early"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Reminder_Window = QtWidgets.QWidget()
    ui = Ui_Reminder_Window()
    ui.setupUi(Reminder_Window)
    Reminder_Window.show()
    sys.exit(app.exec_())

