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

from dataloaderinterface import DataLoaderInterface
import os, sys, datetime

# sys.path.append('../logic')
#from ..logic import patient
from logic.patient import Patient
from logic.photoset import Photoset
from logic.physician import Physician

class FS(DataLoaderInterface):
    """A filesystem manager"""

    # Initialize and do appropriate operations on startup
    def __init__(self, root):
        # Where the FS storage is located
        self.root = root;

        exists = os.path.isdir(root)

        if not exists:
            print "FS: root directory does not exist, creating " + self.root
            self.new_FS = True

            # create the root directory
            os.mkdir(root)
            # there is nothing more to do until the user adds data
        else:
            self.new_FS = False

        return

    # Cleanup/validation before program termination
    def exit(self):
        return

    # Returns if the data storage existed prior to class init
    def is_new(self):
        return self.new_FS

    # Returns a list of all the patients
    def load_all_patients(self):
        # There is nothing to load
        if self.is_new():
            return None

        patients = []

        items = os.listdir(self.root)
        # TODO: Probably not right
        for i in items:
            if os.path.isdir(self.root + "/" + i):
                p = Patient()
                # Parse filename
                p.name_first, p.name_last, p.uid = self.parse_name(i)
                patients.append(p)

        return patients

    def parse_name(self, name):
        unparsed_name = name.split('#')[0]
        unparsed_name = unparsed_name.split()
        name_first = unparsed_name[1]
        name_last = unparsed_name[0][:-1]
        uid = int(name.split('#')[1])

        return [name_first, name_last, uid]

    def parse_names(self, names):
        unparsed_name_list = names.split('\n')
        parsed_name_list = []
        for i in unparsed_name_list:
            parsed_name_list.append( self.parse_name(i) )

        return parsed_name_list

    def generate_patient_dir(self, patient):
        return self.root + "/" + patient.name_last + ", " + patient.name_first + "#" + str(patient.uid)

    def generate_photoset_dir(self, photoset):
        directory = self.generate_patient_dir(photoset.patient)
        uid = str(photoset.uid)
        if os.path.isdir(directory):
            items = os.listdir(directory)
            for i in items:
                if os.path.isdir(directory + "/" + i):
                    #if i.split("#") == uid:
                    return directory + "/" + i
        

    def get_patient_data_from_field(self, patient, field):
        if self.is_new():
            # TODO: error codes
            return None

        directory = self.generate_patient_dir(patient)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/" + field)
                data = f.read()
                f.close()
            except IOError as (errno, strerror):
                print "IOError [{0}]: {1}".format(errno, strerror)
                # TODO: error codes
                return None
                
            return data
        else:
            # TODO: error codes
            print "could not access: " + directory
            return None

        
    def load_patient_notes(self, patient):
        return self.get_patient_data_from_field(patient, "notes.txt")

    def load_patient_physicians(self, patient):
        data = self.get_patient_data_from_field(patient, "physicians.txt")
        physicians = list()
        if data is None:
            # TODO error?
            return None
        else:
            data = self.parse_names(data)
            for i in data:
                d = Physician()
                d.first_name, d.last_name, d.uid = i
                physicians.append(d)
                #patient.physicians.append( d )
                #print patient.physicians
            return physicians
    
    def load_patient_photoset_list(self, patient):
        # not done
        if self.is_new():
            return None

        directory = self.generate_patient_dir(patient)
        if os.path.isdir(directory):
            try:
                items = os.listdir(directory)
                for i in items:
                    if os.path.isdir(directory + "/" + i):
                        p = Photoset()
                        p.patient = patient
                        p.dm = patient.dm
                        #print i
                        split_name = i.split("#")
                        uid = split_name[1]
                        p.uid = uid
                        # p.uid = 0

                        # determine date
                        date = split_name[0].split("-")
                        p.date = datetime.date(int(date[2]), int(date[1]), int(date[0])) # year, month, day
                        patient.photosets |= set([p])
            except IOError as (errno, strerror):
                print "IOError [{0}]: {1}".format(errno, strerror)

    def load_photoset_tags(self, photoset):
        if self.is_new():
            # TODO: error codes
            return None

        directory = self.generate_photoset_dir(photoset)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/diagnoses.txt")
                data = f.read()
                f.close()
            except IOError as (errno, strerror):
                print "IOError [{0}]: {1}".format(errno, strerror)
                # TODO: error codes
                return None
                
            try:
                f = open(directory + "/treatments.txt")
                data = data + "\n" + f.read()
                f.close()
            except IOError as (errno, strerror):
                print "IOError [{0}]: {1}".format(errno, strerror)
                # TODO: error codes
                return None

            data = data.splitlines()
            return data
        else:
            # TODO: error codes
            print "could not access: " + directory 
            return None

    def load_photoset_diagnoses(self, photoset):
        if self.is_new():
            # TODO: error codes
            return None

        directory = self.generate_photoset_dir(photoset)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/diagnoses.txt")
                data = f.read()
                f.close()
            except IOError as (errno, strerror):
                print "IOError [{0}]: {1}".format(errno, strerror)
                # TODO: error codes
                return None

            data = data.splitlines()
            return data
        else:
            # TODO: error codes
            print "could not access: " + directory 
            return None

    def load_photoset_treatments(self, photoset):
        if self.is_new():
            # TODO: error codes
            return None

        directory = self.generate_photoset_dir(photoset)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/treatments.txt")
                data = f.read()
                f.close()
            except IOError as (errno, strerror):
                print "IOError [{0}]: {1}".format(errno, strerror)
                # TODO: error codes
                return None

            data = data.splitlines()
            return data
        else:
            # TODO: error codes
            print "could not access: " + directory 
            return None
