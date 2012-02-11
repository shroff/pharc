import sqlite3

class DB:
	"""A sqlite3 wrapper"""

	def __init__(self):
		exists = True

		try:
			f = open("db.sqlite")
		except IOError:
			exists = False;

		if(exists == True):
			f.close()

		# Open database
		self.connection = sqlite3.connect("db.sqlite")
		# Create object to make queries to the database
		self.cursor = self.connection.cursor()

