#!/usr/bin/env python3
import pymongo
import hashlib
import uuid

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
        self.note_hash = kwargs['note_hash']
        self.note_text = kwargs['note_text']
        self.from_client_id = kwargs['from_client_id']
        self.window_title = kwargs['window_title']
        self.process_name = kwargs['process_name']

    def __iter__(self):
        for key in self.__dict__:
            yield (key, self.__dict__[key])


class Reminder_Info:
    def __init__(self, **kwargs):
        self.note_hash = kwargs['note_hash']
        self.window_title = kwargs['window_title']
        self.process_name = kwargs['process_name']
        self.event_name = kwargs['event_name']
        self.repetition = kwargs['repetition']
        # self.email = kwargs['email']
        self.reminder_time = kwargs['reminder_time']
        self.target_date = kwargs['target_date']
        self.target_time = kwargs['target_time']

    def __iter__(self):
        for key in self.__dict__:
            yield (key, self.__dict__[key])


class Online_Log:
    def __init__(self, **kwargs):
        self.from_client_id = kwargs['from_client_id']
        self.to_client_id = kwargs['to_client_id']
        self.note_hash = kwargs['note_hash']
        self.note_text = kwargs['note_text']

    def __iter__(self):
        for key in self.__dict__:
            yield (key, self.__dict__[key])


class Saved_Password:
    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.password = kwargs['password']

    def __iter__(self):
        for key in self.__dict__:
            yield (key, self.__dict__[key])


class Login_Credentials:
    def __init__(self, **kwargs):
        self.client_id = kwargs['client_id']
        self.token = kwargs['token']

    def __iter__(self):
        for key in self.__dict__:
            yield (key, self.__dict__[key])


class Note:
    def __init__(self, **kwargs):
        self.create_time = kwargs['create_time']
        self.note_text = kwargs['note_text']
        self.process_name = kwargs['process_name']
        self.window_title = kwargs['window_title']
        self.note_hash = self.calc_hash(process_name=self.process_name, window_title=self.window_title)

    def __iter__(self):
        for key in self.__dict__:
            yield (key, self.__dict__[key])

    def calc_hash(self, **kwargs):
        sha256 = hashlib.sha256()
        sha256.update((kwargs['process_name'] + kwargs['window_title']).encode('utf-8'))
        note_hash = sha256.hexdigest()
        return note_hash

    # For testing
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and dict(self) == dict(other))

    def __setitem__(self, key, val):
        setattr(self, key, val)

    def __getitem__(self, key):
        return getattr(self, key)


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
        self.login_credentials_collection = self.db.login_credentials_collection

        if (self.login_credentials_collection.count() == 0):  # First time running the app
            login_credentials_dict = {"client_id": uuid.uuid1().hex, "token": "0"}
            # login_credentials_dict = {"client_id" : "f810faec012011e79ccf2c337a10157b", "token" : "0"}

            self.login_credentials_collection.insert_one(dict(login_credentials_dict))
            print("New client id created!!!!!!!!!!")
        else:
            print("Using old client id!!!!")

        self.login_credentials_dict = self.login_credentials_collection.find_one({})
        self.client_id = self.login_credentials_dict["client_id"]

        self.notes_collection = self.db.notes_collection_temp3

        self.log_collection = self.db.log_collection_temp3

        self.saved_password_collection = self.db.saved_password_collection

        self.reminder_collection = self.db.reminder_collection

    def delete_saved_password(self):
        self.saved_password_collection.delete_many({})

    def read_saved_password(self):
        saved_login_info_dict = self.saved_password_collection.find_one({})
        if (saved_login_info_dict == None):
            return None
        else:
            return Saved_Password(**saved_login_info_dict)

    def insert_saved_password(self, username, password):
        self.saved_password_collection.delete_many({})
        saved_login_info_dict = {"username": username, "password": password}
        return self.saved_password_collection.insert_one(dict(saved_login_info_dict))

    def read_login_credentials(self):
        login_credentials_dict = self.login_credentials_collection.find_one({})
        return Login_Credentials(**login_credentials_dict)

    def update_login_token(self, token):
        self.login_credentials_collection.find_one_and_replace({'client_id': self.client_id},
                                                               {'client_id': self.client_id, 'token': token})

    def delete_login_token(self):
        self.login_credentials_collection.find_one_and_replace({'client_id': self.client_id},
                                                               {'client_id': self.client_id, 'token': ""})

    def close(self):
        self.db_client.close()

    def insert_note(self, note):
        return self.notes_collection.insert_one(dict(note))

    def read_note(self, note_hash):
        note_dict = self.notes_collection.find_one({'note_hash': note_hash})
        print("read note")
        if not note_dict:
            return None
        return Note(**note_dict)

    def update_note(self, note):
        self.notes_collection.find_one_and_replace({'note_hash': note.note_hash}, dict(note))

    def delete_note(self, note_hash):
        self.notes_collection.find_one_and_delete({'note_hash': note_hash})

    def insert_log(self, local_log):
        return self.log_collection.insert_one(dict(local_log))

    def read_log(self, note_hash):
        log_dict = self.log_collection.find_one({'note_hash': note_hash})
        print("read log")
        if not log_dict:
            return None
        return Local_Log(**log_dict)

    def update_log(self, local_log):
        self.log_collection.find_one_and_replace({'note_hash': local_log.note_hash}, dict(local_log))

    def delete_log(self, note_hash):
        self.log_collection.find_one_and_delete({'note_hash': note_hash})

    def delete_note(self, note_hash):
        self.log_collection.find_one_and_delete({'note_hash': note_hash})

    def insert_reminder(self, reminder_info):
        return self.reminder_collection.insert_one(dict(reminder_info))

    def read_reminder(self):
        try:
            reminder_dict = self.reminder_collection.find().sort([('target_date', 1), ('target_time', 1)]).limit(
                1).next()
        except StopIteration:
            return None
        return Reminder_Info(**reminder_dict)

    def delete_reminder(self, note_hash, target_date, target_time):
        self.reminder_collection.find_one_and_delete(
            {'note_hash': note_hash, 'target_date': target_date, 'target_time': target_time})

    def update_reminder(self, note_hash, event_name, reminder_log):
        self.reminder_collection.find_one_and_replace({'note_hash': note_hash, 'event_name': event_name},
                                                      dict(reminder_log))
