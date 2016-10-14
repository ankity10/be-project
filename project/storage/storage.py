import pymongo
import datetime

class notes:
	def __init__(self, note_hash = None, note_attr_obj = None, window_attr_obj = None):
		self.note_hash = note_hash
		self.note_attr_obj = note_attr_obj
		self.window_attr_obj = window_attr_obj

	def return_dict(self):
		d = {}
		d['note_hash'] = self.note_hash
		d['note_attr_obj'] = self.note_attr_obj.return_dict()
		d['window_attr_obj'] = self.window_attr_obj.return_dict()
		return d


	#For testing
	def __eq__(self, other):
		return (isinstance(other, self.__class__) and
			self.return_dict() == other.return_dict())
		
		# return self.__dict__

	def return_obj(self, d):
		self.note_hash = d['note_hash']
		obj_note = note_attr()
		self.note_attr_obj = obj_note.return_obj(d['note_attr_obj'])
		obj_window = window_attr()
		self.window_attr_obj = obj_window.return_obj(d['window_attr_obj'])
		return self


class note_attr:
	def __init__(self, note_color = None, note_time = None, note_info = None):
		# self.note_color = note_color
		self.note_time = note_time
		self.note_info = note_info

	def return_dict(self):
		'''
		d = {}
		d['note_color'] = self.note_color
		d['note_time'] = self.note_time
		d['note_info'] = self.note_info
		return d
		'''
		return self.__dict__

	def return_obj(self, d):
		# self.note_color = d['note_color']
		self.note_time = d['note_time']
		self.note_info = d['note_info']
		return self


class window_attr:
	def __init__(self, process_name = None, window_title = None):
		self.process_name = process_name
		self.window_title = window_title

	def return_dict(self):
		'''
		d = {}
		d['process_name'] = self.process_name
		d['window_title'] = self.window_title
		return d
		'''
		return self.__dict__

	def return_obj(self, d):
		self.process_name = d['process_name']
		self.window_title = d['window_title']
		return self


class db_api:
	def __init__(self):
		# Connection to Mongo DB
		try:
		    conn = pymongo.MongoClient()
		    print ("Connected successfully!!!")
		except (pymongo.errors.ConnectionFailure, e):
			print ("Could not connect to MongoDB: %s" % e) 

		db = conn.notes_db
		self.collection = db.notes_collection

	def write_note_to_db(self, note_obj):    
		d = note_obj.return_dict()
		self.collection.insert_one(d)

	def read_note_from_db(self, note_hash):
		note_obj_dict = self.collection.find_one({'note_hash' : note_hash})
		if not note_obj_dict:
			return None
		note_obj = notes()
		note_obj = note_obj.return_obj(note_obj_dict)
		return note_obj

	def delete_note(self, note_hash):
		note_obj_dict = self.collection.find_one_and_delete({'note_hash' : note_hash})

	def update_note(self, note_hash, note_obj):
		new_dict = note_obj.return_dict()
		self.collection.find_one_and_replace({'note_hash' : note_hash}, new_dict)

	def insert(self, hash, text, time, window_title, process_name):
		note_attr_obj = note_attr(None, time, text)

		window_attr_obj = window_attr(process_name, window_title)
		note = notes(hash, note_attr_obj, window_attr_obj)
		self.write_note_to_db(note)

	def update(self, hash, text, time, window_title, process_name):
		note_attr_obj = note_attr(None, time, text)
		window_attr_obj = window_attr(process_name, window_title)
		note = notes(hash, note_attr_obj, window_attr_obj)

		self.update_note(hash, note)
	