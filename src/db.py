import sqlite3

class DB:
	"""A sqlite3 wrapper"""

	def __init__(self):

		# Check if the DB exists before we open it
		exists = True
		try:
			f = open("db.sqlite")
		except IOError:
			exists = False;

		# If the DB file already exists, we need to close f
		if(exists == True):
			f.close()

		# Open database or create it if it didn't exist
		self.connection = sqlite3.connect("db.sqlite")
		# Create object to make queries to the database
		self.cursor = self.connection.cursor()

		# Create tables if the DB didn't exist
		if(exists == False):
			# Indicate there is nothing to load from the DB
			self.new_DB = True
		else:
			# Indicate there are things to load from the DB
			self.newDB = False
			
	def exit(self):
		# Close the DB cursor
		self.cursor.close()

