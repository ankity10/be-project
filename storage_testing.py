import unittest
import random
from random import randint
import string
import datetime 
import storage_api as api

def gen_length():
	return randint(2,20)

def gen_string():
	length = gen_length()
	s=string.lowercase + string.uppercase + string.digits
	return ''.join(random.sample(s,10))
	# return ''.join(random.choice(string.lowercase) for i in range(length))

def gen_date():
	year = randint(2000,2020)
	month = randint(1,12)
	date = randint(1,28)
	hr = randint(0,23)
	mn = randint(0,59)
	sec = randint(0,59)
	return datetime.datetime(year, month, date, hr, mn, sec)

class testing(unittest.TestCase):
	def test_readwrite(self):
		obj = []
		api_obj = api.db_api()
		for i in range(0,10):
			note_hash = i
			note_color = gen_string()
			note_time = gen_date()
			note_info = gen_string()
			note_attr_obj = api.note_attr(note_color, note_time, note_info)
			process_name = gen_string()
			window_title = gen_string()
			window_attr_obj = api.window_attr(process_name, window_title)
			notes_obj = api.notes(note_hash, note_attr_obj, window_attr_obj)

			obj.append(notes_obj)
			api_obj.write_note_to_db(notes_obj)

		self.assertEqual(api_obj.read_note_from_db(0), obj[0])
		self.assertEqual(api_obj.read_note_from_db(1), obj[1])
		self.assertEqual(api_obj.read_note_from_db(2), obj[2])
		self.assertEqual(api_obj.read_note_from_db(3), obj[3])
		self.assertEqual(api_obj.read_note_from_db(4), obj[4])
		self.assertEqual(api_obj.read_note_from_db(5), obj[5])
		self.assertEqual(api_obj.read_note_from_db(6), obj[6])
		self.assertEqual(api_obj.read_note_from_db(7), obj[7])
		self.assertEqual(api_obj.read_note_from_db(8), obj[8])
		self.assertEqual(api_obj.read_note_from_db(9), obj[9])

	def test_update(self):
		api_obj = api.db_api()
		obj = []
		for i in range(0,10):
			note_hash = i
			note_color = gen_string()
			note_time = gen_date()
			note_info = gen_string()
			note_attr_obj = api.note_attr(note_color, note_time, note_info)
			process_name = gen_string()
			window_title = gen_string()
			window_attr_obj = api.window_attr(process_name, window_title)
			notes_obj = api.notes(note_hash, note_attr_obj, window_attr_obj)

			obj.append(notes_obj)
			api_obj.update_note(i, notes_obj)

		self.assertEqual(api_obj.read_note_from_db(0), obj[0])
		self.assertEqual(api_obj.read_note_from_db(1), obj[1])
		self.assertEqual(api_obj.read_note_from_db(2), obj[2])
		self.assertEqual(api_obj.read_note_from_db(3), obj[3])
		self.assertEqual(api_obj.read_note_from_db(4), obj[4])
		self.assertEqual(api_obj.read_note_from_db(5), obj[5])
		self.assertEqual(api_obj.read_note_from_db(6), obj[6])
		self.assertEqual(api_obj.read_note_from_db(7), obj[7])
		self.assertEqual(api_obj.read_note_from_db(8), obj[8])
		self.assertEqual(api_obj.read_note_from_db(9), obj[9])

	def test_delete(self):
		api_obj = api.db_api()
		for i in range(0,10):		
			api_obj.delete_note(i)

		self.assertEqual(api_obj.read_note_from_db(0), None)
		self.assertEqual(api_obj.read_note_from_db(1), None)
		self.assertEqual(api_obj.read_note_from_db(2), None)
		self.assertEqual(api_obj.read_note_from_db(3), None)
		self.assertEqual(api_obj.read_note_from_db(4), None)
		self.assertEqual(api_obj.read_note_from_db(5), None)
		self.assertEqual(api_obj.read_note_from_db(6), None)
		self.assertEqual(api_obj.read_note_from_db(7), None)
		self.assertEqual(api_obj.read_note_from_db(8), None)
		self.assertEqual(api_obj.read_note_from_db(9), None)			



if __name__ == '__main__':
	unittest.main()

