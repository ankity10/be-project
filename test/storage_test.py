import unittest
import string
import datetime
import sys
import random
from random import randint
from storage import Note, Db


def gen_length():
    return randint(2, 20)


def gen_string():
    length = gen_length()
    s = string.ascii_letters
    return ''.join(random.sample(s, length))


def gen_date():
    year = randint(2000, 2020)
    month = randint(1, 12)
    date = randint(1, 28)
    hr = randint(0, 23)
    mn = randint(0, 59)
    sec = randint(0, 59)
    return datetime.datetime(year, month, date, hr, mn, sec)


class DbTest(unittest.TestCase):
    db = Db()
    note_list = []

    def setUp(self):
        d = {}
        for i in range(0, 10):
            d['create_time'] = gen_date()
            d['text'] = gen_string()
            d['process_name'] = gen_string()
            d['window_title'] = gen_string()
            note = Note(**d)
            self.note_list.append(note)
            self.db.insert_note(self.note_list[i])

    def tearDown(self):
        self.db.close()

    def test_read_write(self):
        for i in range(0, 10):
            self.assertEqual(self.db.read_note(self.note_list[i].hash_value), self.note_list[i])

    def test_update(self):
        for i in range(0, 10):
            self.note_list[i].text = gen_string()
            self.db.update_note(self.note_list[i])
            self.assertEqual(self.db.read_note(self.note_list[i].hash_value), self.note_list[i])

    def test_delete(self):
        for i in range(0, 10):
            self.db.delete_note(self.note_list[i].hash_value)
            self.assertEqual(self.db.read_note(self.note_list[i].hash_value), None)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(DbTest))
    return test_suite


if __name__ == '__main__':
    if '-v' in sys.argv:
        runner = unittest.TextTestRunner(verbosity=2)
    else:
        runner = unittest.TextTestRunner()
    runner.run(suite())
