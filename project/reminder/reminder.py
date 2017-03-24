from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import time
import threading
from storage.storage import *
import datetime
from ui.qt.Reminder_Window import Ui_Reminder_Window


class Reminder(QWidget):
	def __init__(self, main_app):
		super().__init__()
		print("In reminder")
		self.repetition_text = 0
		self.reminder_text = 0
		self.main_app = main_app
		self.thread_start = 0
		self.setWindowTitle("Reminder")
		# self.setWindowFlags(Qt.FramelessWindowHint)
		self.setupUI()

	def setupUI(self):
		print("UI reminder")
		# p = self.palette()
		# p.setColor(self.backgroundRole(), Qt.white)
		# self.setPalette(p)
		# self.setStyleSheet("""
		# 	.QWidget {
		# 	"background-color: rgb(175, 238, 238);"
		# 	}
		# 	""")
		# self.setStyleSheet("background-color : rgb(224, 255, 255);")
		self.reminder_ui = Ui_Reminder_Window()
		self.reminder_ui.setupUi(self)

		self.setFixedSize(400,300)
		# self.event_title_label = QLabel("Event name", self)
		# self.event_title_label.move(5,10)

		# self.event_title_edit = QLineEdit(self)
		# self.event_title_edit.setStyleSheet("background-color : rgb(240, 255, 255")
		# self.event_title_edit.setPlaceholderText("Event name")
		# self.event_title_edit.setMinimumWidth(10)
		# self.event_title_edit.move(100,5)
		# self.event_title = self.event_title_edit.text()

		# self.target_date_label = QLabel("Date",self)
		# self.target_date_label.move(5, 35)

		# self.target_date = QDateEdit(self)
		# self.target_date.setStyleSheet("background-color : rgb(240, 255, 255")
		self.reminder_ui.target_date_edit.setDate(QDate.currentDate())
		self.target_date_selected = QDate.currentDate()
		self.reminder_ui.target_date_edit.setMinimumDate(QDate.currentDate())
		# self.target_date.setCalendarPopup(True)
		self.reminder_ui.target_date_edit.setDisplayFormat('dd/MM/yyyy')
		self.reminder_ui.target_date_edit.cal = self.reminder_ui.target_date_edit.calendarWidget()
		self.reminder_ui.target_date_edit.cal.setFirstDayOfWeek(Qt.Monday)
		self.reminder_ui.target_date_edit.cal.setHorizontalHeaderFormat(QCalendarWidget.SingleLetterDayNames)
		self.reminder_ui.target_date_edit.cal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
		self.reminder_ui.target_date_edit.cal.setGridVisible(True)
		self.reminder_ui.target_date_edit.dateChanged.connect(self.date_selected)
		# self.target_date.move(50, 30)
		
		# self.target_time_label = QLabel("Time", self)
		# self.target_time_label.move(200,35)
		
		# self.target_time = QTimeEdit(self)
		# self.target_time.setStyleSheet("background-color : rgb(240, 255, 255")
		self.reminder_ui.target_time_edit.setTime(QTime.currentTime())
		# # if(self.target_date_selected == QDate.currentDate())
		# # 	self.target_time.setMinimumTime(QTime.currentTime())
		self.target_time_selected = QTime.currentTime()
		self.reminder_ui.target_time_edit.timeChanged.connect(self.time_selected)

		self.reminder_ui.more_options_button.clicked.connect(self.more_options_method)
		self.reminder_ui.less_options_button.hide()
		self.reminder_ui.less_options_button.clicked.connect(self.less_options_method)
		self.reminder_ui.repetition_label.hide()
		self.reminder_ui.reminder_label.hide()
		self.reminder_ui.repetition_options.hide()
		self.reminder_ui.reminder_options.hide()
		self.reminder_ui.repetition_options.activated.connect(self.repetition_selected)
		self.reminder_ui.reminder_options.activated.connect(self.reminder_selected)
		if(self.target_date_selected == QDate.currentDate()):
			self.reminder_ui.target_time_edit.setMinimumTime(QTime.currentTime())
		else:
			t = QTime(0,0,0)
			self.reminder_ui.target_time_edit.setMinimumTime(t)

		# self.target_time.move(230,30)
		# if(self.target_date_selected == QDate.currentDate()):
		# 	print("INNNNN")
		# 	self.reminder_ui.target_time_edit.setMinimumTime(QTime.currentTime())
		# # self.target_time.setTimeRange(QTime(1,0,0,0),QTime(12,59,0,0))

		# self.reminder_ui.repetition_label = QLabel("Repetition", self)
		# self.reminder_ui.repetition_label.move(5,60)

		# self.repetition = QComboBox(self)
		# self.repetition.setStyleSheet("background-color : rgb(240, 255, 255")
		# self.repetition.addItem("One-Time event")
		# self.repetition.addItem("Daily")
		# self.repetition.addItem("Weekly")
		# self.repetition.addItem("Monthly")
		# self.repetition.move(100,55)
		# self.repetition.setCurrentIndex(0)
		
		# self.reminder_ui.reminder_label = QLabel("Repetition", self)
		# self.reminder_ui.reminder_label.move(5,80)

		# self.reminder = QComboBox(self)
		# self.reminder.setMinimumWidth(30)
		# self.reminder.setStyleSheet("background-color : rgb(240, 255, 255")
		# self.reminder.addItem("On time")
		# self.reminder.addItem("5 mins early")
		# self.reminder.addItem("10 mins early")
		# self.reminder.addItem("1 hour early")
		# self.reminder.addItem("2 hour early")
		# self.reminder.addItem("1 day early")
		# self.reminder.move(100,80)
		# self.reminder.setCurrentIndex(0)
		

		# self.reminder_ui.add_button = QPushButton("ADD",self)
		# self.reminder_ui.add_button.move(30,120)
		self.reminder_ui.add_button.clicked.connect(self.reminder_added)
		self.reminder_ui.add_button.move(230,240)
		# self.reminder_ui.add_button.setStyleSheet("background-colorer : rgb(240, 255, 255")

		# self.reminder_ui.cancel_button = QPushButton("CANCEL", self)
		# self.reminder_ui.cancel_button.move(120, 120)
		self.reminder_ui.cancel_button.clicked.connect(self.cancel_method)
		self.reminder_ui.cancel_button.move(40,240)
		# self.reminder_ui.cancel_button.setStyleSheet("background-color : egb(240, 255, 255")
		if(self.target_date_selected == QDate.currentDate()):
			self.reminder_ui.reminder_options.model().item(5).setEnabled(False)

		self.move(QApplication.desktop().screen().rect().center()- self.rect().center())

		# self.move(400,250)
		self.show()

	def more_options_method(self):
		self.reminder_ui.less_options_button.show()
		self.reminder_ui.repetition_options.show()
		self.reminder_ui.reminder_options.show()
		self.reminder_ui.reminder_label.show()
		self.reminder_ui.repetition_label.show()
		self.reminder_ui.more_options_button.hide()
		self.setFixedSize(400,380)
		self.reminder_ui.add_button.move(40,320)
		self.reminder_ui.cancel_button.move(230,320)

	def less_options_method(self):
		self.reminder_ui.less_options_button.hide()
		self.reminder_ui.repetition_options.hide()
		self.reminder_ui.reminder_options.hide()
		self.reminder_ui.reminder_label.hide()
		self.reminder_ui.repetition_label.hide()
		self.reminder_ui.more_options_button.show()
		self.setFixedSize(400,300)
		self.reminder_ui.cancel_button.move(40,240)
		self.reminder_ui.add_button.move(230,240)


	def date_selected(self, date):
		self.target_date_selected = date
		if(self.target_date_selected == QDate.currentDate()):
			self.reminder_ui.target_time_edit.setMinimumTime(QTime.currentTime())
		else:
			t = QTime(0,0,0)
			self.reminder_ui.target_time_edit.setMinimumTime(t)

		if(self.target_date_selected > QDate.currentDate()):
			self.reminder_ui.reminder_options.model().item(5).setEnabled(True)

	def time_selected(self, time):
		self.target_time_selected = time

	def repetition_selected(self, text):
		self.repetition_text = text
		print(self.repetition_text)

	def reminder_selected(self, text):
		self.reminder_text = text
		print(self.reminder_text)

	def cancel_method(self):
		self.close()

	def reminder_added(self):
		self.event_title = self.reminder_ui.event_title_edit.text()
		self.reminder_selection_method()
		self.main_app.reminder_thread_start = 0
		self.store_reminder()
		if(self.main_app.recent_reminder == None):
			self.main_app.reminder_thread_start =1
			# self.main_app.reminder_thread_start = 1
			t = threading.Thread(target = self.main_app.set_reminder)
			t.start()
		self.close()
		# t = threading.Thread(target=self.set_reminder)
		# t.start()

	def store_reminder(self):
		reminder_dict_info = {}
		target_py_time = self.target_time_selected.toPyTime()
		target_time = target_py_time.strftime('%H-%M')
		target_py_date = self.target_date_selected.toPyDate()
		target_date = target_py_date.strftime('%m-%d-%Y')
		# rem_exist = self.main_app.storage.find_reminder(self.event_title, target_date, target_time)
		# print(rem_exist)
		# print("--------check")
		self.main_app.new_rem_entry = 1
		# if(self.main_app.recent_reminder != None):
		# 	print("----------------In less------------")
		# 	running_rem_date = datetime.datetime.strptime(self.main_app.recent_reminder.target_date, '%m-%d-%Y').date()
		# 	running_rem_time = datetime.datetime.strptime(self.main_app.recent_reminder.target_time, '%H-%M').time()
		# 	if(target_py_date < running_rem_date):
		# 		print("------------------Yes less ------------------")
		# 		self.main_app.new_rem_entry = 1
		# 	elif(target_py_date == running_rem_date and target_py_time < running_rem_time):
		# 		print("------------------Yes less ------------------")
		# 		self.main_app.new_rem_entry = 1


		window_title = self.main_app.wirm.prev_active_window_title
		process_name = self.main_app.wirm.prev_active_window_name
		print(window_title)
		print(process_name)
		note_hash = self.main_app.calc_hash(process_name = process_name, window_title = window_title)
		reminder_dict_info = {"note_hash" : note_hash, "window_title" : window_title,
						"process_name": process_name, "event_name" : self.event_title, "repetition": self.repetition_text,
						"reminder_time" : self.reminder_text, "target_date" : target_date,
						"target_time" : target_time}
		reminder_dict = Reminder_Info(**reminder_dict_info)
		self.main_app.storage.insert_reminder(reminder_dict)



	# def store_reminder_again():


	def repetition_selection_method(self):
		if(self.repetition_text == 1):
			self.target_date_selected.setDate(self.target_date_selected.year(),self.target_date_selected.month(),self.target_date_selected.day()+1)
		elif(self.reminder_text == 2):
			self.target_date_selected.setDate(self.target_date_selected.year(),self.target_date_selected.month(),self.target_date_selected.day()+7)
		elif(self.reminder_text == 3):
			self.target_date_selected.setDate(self.target_date_selected.year(),self.target_date_selected.month()+1,self.target_date_selected.day())


	def reminder_selection_method(self):
		if(self.reminder_text == 1):
			self.target_time_selected.setHMS(self.target_time_selected.hour(), self.target_time_selected.minute()-5, 0)
		elif(self.reminder_text == 2):
			self.target_time_selected.setHMS(self.target_time_selected.hour(), self.target_time_selected.minute()-10, 0)
		elif(self.reminder_text == 3):
			self.target_time_selected.setHMS(self.target_time_selected.hour()-1, self.target_time_selected.minute(), 0)
		elif(self.reminder_text == 4):
			self.target_time_selected.setHMS(self.target_time_selected.hour()-2, self.target_time_selected.minute()-5, 0)
		elif(self.reminder_text == 5):
			self.target_date_selected.setDate(self.target_date_selected.year(),self.target_date_selected.month(),self.target_date_selected.day()-1)

	# def set_reminder(self):
	# 	# while(self.thread_start == 1):
	# 	print("In thread")
	# 	reminder = self.main_app.storage.read_reminder()
	# 	if(reminder):
	# 		print("reminder")
	# 		print(reminder.target_date)
	# 		target_date = datetime.datetime.strptime(reminder.target_date, '%m-%d-%Y').date()
	# 		target_time = datetime.datetime.strptime(reminder.target_time, '%H-%M').time()
	# 		while(QDate.currentDate().toPyDate() < target_date):
	# 			time.sleep(5)
	# 		print("Date")
	# 		current_time = QTime.currentTime().toPyTime()
	# 		while(current_time.hour < target_time.hour):
	# 			time.sleep(5)
	# 			current_time = QTime.currentTime().toPyTime()
	# 		print("Hour")
	# 		current_time = QTime.currentTime().toPyTime()
	# 		while(current_time.minute < target_time.minute):
	# 			time.sleep(5)
	# 			current_time = QTime.currentTime().toPyTime()
	# 		print("Minute")
	# 		msg = QMessageBox()
	# 		msg.setText("Its time")
	# 		msg.setStandardButtons(QMessageBox.Ok)
	# 		 # msg.buttonClicked.connect(self.close_thread)
	# 		msg.exec_()
	# 		# if(self.repetition_text != 0):
	# 		# 	self.repetition_selection_method()
	# 		# 	self.set_reminder()
	# 		self.main_app.storage.delete_reminder(reminder.note_hash, reminder.target_date, reminder.target_time)
	# 	# 	else:
	# 	# 		self.thread_start = 0
	# 	# # 
	# 	# 
	# 	# self.close_thread()

	def close_thread(self):
		self.close()
		sys.exit(0)


def main():
    app = QApplication(sys.argv)
    ex = Reminder()
    ex.show()
    app.exec_()


if __name__ == '__main__':
    main()
