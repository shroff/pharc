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
					name text primary key asc not null,
					id int not null
					);

				create table doctors(
					name text not null,
					id int primary key not null
					);
				
				create table diagnoses(
					name text not null,
					id int primary key not null
					);

				create table treatments(
					name text not null,
					id int primary key not null
					);

				create table photosets(
					date int not null,
					direcotry_hash text,
					diagnosis_txt_hash text,
					physicians_txt_hash text,
					treatment_txt_hash text,
					id int primary key not null,
					path text not null
					);

				create table photos(
					id int primary key not null,
					path text not null,
					hash text not null
					);

				create table configuration(
					root_dor text not null,
					new_image_dir text not null,
					last_user text not null,
					current_user text not null,
					db_version text not null
					);

				create table users(
					name text primary key not null,
					id not null
					);

				create table thumbnails(
					id not null,
					path not null
				""")

			self.connection.commit()

		else:
			# Indicate there are things to load from the DB
			self.newDB = False
	
	def exit(self):
		# Close the DB cursor
		self.cursor.close()

