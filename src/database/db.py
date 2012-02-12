# PHARC: a photo archiving application for physicians
# Copyright (C) 2012  Saul Reynolds-Haertle, James Cline
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import sqlite3

from dataloaderinterface import DataLoaderInterface

class DB (DataLoaderInterface):
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
					id int unique not null
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
					path text unique not null,
					patient int references patients(id) on delete cascade on update cascade,
					notes text
					);

				create table photos(
					id int primary key not null,
					path text unique not null,
					hash text unique not null,
					photoset int references photosets(id) on delete cascade on update cascade
					);

				create table configuration(
					root_dir text not null,
					new_image_dir text not null,
					last_user text,
					current_user text not null,
					db_version text not null
					);

				create table users(
					name text primary key not null,
					id unique not null
					);

				create table thumbnails(
					id unique not null,
					path unique not null
					);
				""")

			self.connection.commit()

		else:
			# Indicate there are things to load from the DB
			self.newDB = False
	
	def exit(self):
		# Close the DB cursor
		self.cursor.close()

	def isNew(self):
		return self.new_DB
