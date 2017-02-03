#!/usr/bin/env python3
import pymongo
import datetime
import hashlib


DEBUG = True
if DEBUG:
	from colorama import init, Fore, Style
	init(autoreset=True)

def dprint(text):
	if DEBUG:
		print(Fore.RED + Style.BRIGHT 
			  + text)

class Local_Log:

	def __init__(self, **kwargs):
		self.hash_value = kwargs['hash_value']
		self.text = kwargs['text']

	def __iter__(self):
		for key in self.__dict__:
			yield(key, self.__dict__[key])

class Online_Log:

	def __init__(self, **kwargs):
		self.from_client_id = kwargs['from_client_id']
		self.to_client_id = kwargs['to_client_id']
		self.note_hash = kwargs['note_hash']
		self.note_text = kwargs['note_text']

	def __iter__(self):
		for key in self.__dict__:
			yield(key, self.__dict__[key])

class Note:

	def __init__(self, **kwargs):
		self.create_time = kwargs['create_time']
		self.text = {}
		self.text = kwargs['text']
		self.process_name = kwargs['process_name']
		self.window_title = kwargs['window_title']
		self.hash_value = self.calc_hash(process_name=self.process_name, window_title=self.window_title)

	def __iter__(self):
		for key in self.__dict__:
			yield(key, self.__dict__[key])

	def calc_hash(self, **kwargs):
		sha256 = hashlib.sha256()
		sha256.update((kwargs['process_name'] + kwargs['window_title']).encode('utf-8'))
		hash_value = sha256.hexdigest()
		return hash_value

	# For testing
	def __eq__(self, other):
		return (isinstance(other, self.__class__) and dict(self) == dict(other))


class Db:

	def __init__(self):
		self.db_client = pymongo.MongoClient(host='localhost',
											 port=27017,
											 connectTimeoutMS=10000, 
											 serverSelectionTimeoutMS=8000)
		try:
			self.db_client.admin.command('ismaster')	
			print("Connected to database....!!")
		except pymongo.errors.ConnectionFailure:
			dprint("Could not connect to MongoDB")
			dprint("Application startup cannot proceed. Apllication is exiting.")
			dprint("Please check your mongoDB connection and try again.")
			exit()

		self.db = self.db_client.notes_db
		self.notes_collection = self.db.notes_collection
		self.log_collection = self.db.log_collection

	def close(self):
		self.db_client.close()

	def insert_note(self, note):
		return self.notes_collection.insert_one(dict(note))

	def read_note(self, hash_value):
		note_dict = self.notes_collection.find_one({'hash_value' : hash_value})
		print("read note")
		if not note_dict:
			return None
		return Note(**note_dict)

	def update_note(self, note):
		self.notes_collection.find_one_and_replace({'hash_value' : note.hash_value}, dict(note))

	def delete_note(self, hash_value):
		self.notes_collection.find_one_and_delete({'hash_value' : hash_value})

	def insert_log(self, local_log):
		return self.log_collection.insert_one(dict(local_log))

	def read_log(self, hash_value):
		log_dict = self.log_collection.find_one({'hash_value' : hash_value})
		print("read log")
		if not log_dict:
			return None
		return Local_Log(**log_dict)

	def update_log(self, local_log):
		self.log_collection.find_one_and_replace({'hash_value' : local_log.hash_value}, dict(local_log))

	def delete_note(self, hash_value):
		self.log_collection.find_one_and_delete({'hash_value' : hash_value})


