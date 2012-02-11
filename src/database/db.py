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
		if exists:
			f.close()

		# Open database or create it if it didn't exist
		self.connection = sqlite3.connect("db.sqlite")
		# Create object to make queries to the database
		self.cursor = self.connection.cursor()

		# Create tables if the DB didn't exist
		if not exists:
			# Indicate there is nothing to load from the DB
			self.new_DB = True
			self.cursor.executescript("""
				create table patients(
					name,
					id int primary key not null
					);

				create table doctors(
					name,
					id int primary key not null
					);
				
				create table diagnoses(
					name,
					id int primary key not null
					);

				create table treatments(
					name,
					id int primary key not null
					);

				create table photosets(
					date,
					direcotry_hash,
					diagnosis_txt_hash,
					physicians_txt_hash,
					treatment_txt_hash,
					id int primary key not null,
					path
					);

				create table photos(
					id int primary key not null,
					path,
					hash
					);

				create table configuration(
					root_dor,
					new_image_dir,
					last_user,
					current_user,
					db_version
					);

				create table users(
					name,
					id
					);
				""")

			self.connection.commit()

		else:
			# Indicate there are things to load from the DB
			self.newDB = False
	
	def getThumbnails(self, patientID):
		if self.newDB:
			return None

	def exit(self):
		# Close the DB cursor
		self.cursor.close()

