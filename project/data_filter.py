import hashlib

class data_filter:
	def __init__(self):
		self.hash = ""
		self.hash_obj = hashlib.sha256()

	def get_hash( self,active_window_name = "",active_window_title =""):
		self.hash_obj.update((active_window_name+active_window_title).encode('utf-8'))
		self.hash = self.hash_obj.hexdigest()
		return self.hash