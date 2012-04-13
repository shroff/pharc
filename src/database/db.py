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

from .dataloaderinterface import DataLoaderInterface

class DB (DataLoaderInterface):
    """A sqlite3 wrapper"""

    # Initialize and do appropriate operations on startup
    def __init__(self, path):

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
        self.connection = sqlite3.connect(path + "db.sqlite")
        # Create object to make queries to the database
        self.cursor = self.connection.cursor()

        # Create tables if the DB didn't exist
        if not exists:
            # Indicate there is nothing to load from the DB
            self.newDB = True
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
                    directoryHash text,
                    diagnosisTxtHash text,
                    physiciansTxtHash text,
                    treatmentTxtHash text,
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
                    rootDir text not null,
                    newImageDir text not null,
                    lastUser text,
                    currentUser text not null,
                    dbVersion text not null
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
    
    # Cleanup/validation before program termination
    def exit(self):
        # Close the DB cursor
        self.cursor.close()

    # Returns if the data storage existed prior to class init
    def isNew(self):
        return self.newDB

    # Returns a list of all the patients
    def loadAllPatients(self):
        if self.isNew():
            return None
        self.cursor.execute("select * from patients");
        patients = []
        for row in self.cursor:
            p = Patient()
            # TODO: this cannot be right...
            name = row[0].split()
            p.nameFirst = name[1]
            p.nameLast = name[0]
            p.uid = row[1]
            patients.append( p )

        return patients

