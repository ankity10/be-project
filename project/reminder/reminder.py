from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import time
import threading
from storage.storage2 import *
import datetime

class Reminder(QWidget):
	def __init__(self, main_app):
		super().__init__()
		print("In reminder")
		self.repetition_text = 0
		self.reminder_text = 0
		self.main_app = main_app
		self.thread_start = 0
		# QMainWindow.__init__(self)
		self.setWindowTitle("Reminder")
		self.setupUI()

	def setupUI(self):
		print("UI reminder")
		# self.setStyleSheet("""
		# 	QWidget {
		# 	"border: 2px solid green;"
		# 	"border-radius: 20px;"
		# 	"padding: 2px;"
		# 	"background-color: rgb(85, 85, 255);"
		# 	}
		# 	""")
		self.setStyleSheet("border : white;")
		self.event_name_label = QLabel("Event name", self)
		self.event_name_label.move(5,10)

		self.event_name_edit = QLineEdit(self)
		self.event_name_edit.setPlaceholderText("Event name")
		self.event_name_edit.setMinimumWidth(10)
		self.event_name_edit.move(100,5)
		self.event_name = self.event_name_edit.text()

		self.target_date_label = QLabel("Date",self)
		self.target_date_label.move(5, 35)

		self.target_date = QDateEdit(self)
		self.target_date.setDate(QDate.currentDate())
		self.target_date_selected = QDate.currentDate()
		self.target_date.setMinimumDate(QDate.currentDate())
		self.target_date.setCalendarPopup(True)
		self.target_date.setDisplayFormat('dd/MM/yyyy')
		self.target_date.cal = self.target_date.calendarWidget()
		self.target_date.cal.setFirstDayOfWeek(Qt.Monday)
		self.target_date.cal.setHorizontalHeaderFormat(QCalendarWidget.SingleLetterDayNames)
		self.target_date.cal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
		self.target_date.cal.setGridVisible(True)
		self.target_date.dateChanged.connect(self.date_selected)
		self.target_date.move(40, 30)
		
		self.target_time_label = QLabel("Time", self)
		self.target_time_label.move(170,35)
		
		self.target_time = QTimeEdit(self)
		self.target_time.setTime(QTime.currentTime())
		self.target_time.setMinimumTime(QTime.currentTime())
		self.target_time.timeChanged.connect(self.time_selected)
		self.target_time.move(200,30)
		# self.target_time.setMinimumTime(QTime.currentTime())
		# self.target_time.setTimeRange(QTime(1,0,0,0),QTime(12,59,0,0))

		self.repetition_label = QLabel("Repetition", self)
		self.repetition_label.move(5,60)

		self.repetition = QComboBox(self)
		self.repetition.addItem("One-Time event")
		self.repetition.addItem("Daily")
		self.repetition.addItem("Weekly")
		self.repetition.addItem("Monthly")
		self.repetition.move(100,55)
		self.repetition.setCurrentIndex(0)
		self.repetition.activated.connect(self.repetition_selected)

		self.reminder_label = QLabel("Repetition", self)
		self.reminder_label.move(5,80)

		self.reminder = QComboBox(self)
		self.reminder.addItem("On time")
		self.reminder.addItem("5 mins early")
		self.reminder.addItem("10 mins early")
		self.reminder.addItem("1 hour early")
		self.reminder.addItem("2 hour early")
		self.reminder.addItem("1 day early")
		self.reminder.move(100,80)
		self.reminder.setCurrentIndex(0)
		self.reminder.activated.connect(self.reminder_selected)

		self.add_button = QPushButton("ADD",self)
		self.add_button.move(5,120)
		self.add_button.clicked.connect(self.reminder_added)

		self.cancel_button = QPushButton("CANCEL", self)
		self.cancel_button.move(50, 120)
		self.cancel_button.clicked.connect(self.cancel_method)
		if(self.target_date_selected == QDate.currentDate()):
			self.reminder.model().item(5).setEnabled(False)

		self.setGeometry(400,250,400,200)
		self.show()

	def date_selected(self, date):
		self.target_date_selected = date
		if(self.target_date_selected > QDate.currentDate()):
			self.reminder.model().item(5).setEnabled(True)

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
		self.reminder_selection_method()
		self.store_reminder()
		if(self.main_app.reminder_thread_start == 0):
			self.main_app.reminder_thread_start =1
			t = threading.Thread(target = self.main_app.set_reminder)
			t.start()
		self.close()
		# t = threading.Thread(target=self.set_reminder)
		# t.start()

	def store_reminder(self):
		reminder_dict_info = {}
		target_time1 = self.target_time_selected.toPyTime()
		target_time = target_time1.strftime('%H-%M')
		target_date1 = self.target_date_selected.toPyDate()
		target_date = target_date1.strftime('%m-%d-%Y')
		window_title = self.main_app.wirm.prev_active_window_title
		process_name = self.main_app.wirm.prev_active_window_name
		print(window_title)
		print(process_name)
		note_hash = self.main_app.calc_hash(process_name = process_name, window_title = window_title)
		reminder_dict_info = {"note_hash" : note_hash, "window_title" : window_title,
						"process_name": process_name, "event_name" : self.event_name, "repetition": self.repetition_text,
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






