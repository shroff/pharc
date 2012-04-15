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

import os, sys, datetime

import logic.patient as patient
import logic.photoset as photoset

class FS:
    """A filesystem manager"""

    # Initialize and do appropriate operations on startup
    def __init__(self, root):
        # Where the FS storage is located
        self.root = root;

        exists = os.path.isdir(root)

        if not exists:
            print("FS: root directory does not exist, creating " + self.root)
            self.newFS = True

            # create the root directory
            os.mkdir(root)
            # there is nothing more to do until the user adds data
        else:
            self.newFS = False

        return

    # Cleanup/validation before program termination
    def exit(self):
        return

    # Returns if the data storage existed prior to class init
    def isNew(self):
        return self.newFS

    def createPhotosetDir(self, photoset, patient=None):
        directory = self.generatePhotosetDir(photoset, patient)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def deletePhotosetDir(self, photoset):
        pass

    # Returns a list of all the patients
    def loadAllPatients(self):
        # There is nothing to load
        if self.isNew():
            return None

        patients = []

        items = os.listdir(self.root)
        # TODO: Probably not right
        for i in items:
            if os.path.isdir(self.root + "/" + i):
                p = patient.Patient()
                # Parse filename
                p.nameFirst, p.nameLast, p.uid = self.parseName(i)
                p.uid = int(p.uid)
                patients.append(p)

        return patients

    def parseName(self, name):
        unparsedName = name.split('#')[0]
        unparsedName = unparsedName.split()
        nameFirst = unparsedName[1]
        nameLast = unparsedName[0][:-1]
        uid = int(name.split('#')[1])

        return [nameFirst, nameLast, uid]

    def parseNames(self, names):
        unparsedNameList = names.split('\n')
        parsedNameList = []
        for i in unparsedNameList:
            parsedNameList.append( self.parseName(i) )

        return parsedNameList

    def generatePatientDir(self, patient):
        return self.root + "/" + patient.nameLast + ", " + patient.nameFirst + "#" + str(patient.uid)

    def generatePhotosetDir(self, ps, p=None):
        if p is None:
            p = ps.patient
        directory = self.generatePatientDir(p)
        uid = str(ps.uid)
        if os.path.isdir(directory):
            items = os.listdir(directory)
            for i in items:
                if os.path.isdir(directory + "/" + i):
                    #if i.split("#") == uid:
                    return directory + "/" + i
        

    def getPatientDataFromField(self, patient, field):
        if self.isNew():
            # TODO: error codes
            return None

        directory = self.generatePatientDir(patient)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/" + field)
                data = f.read()
                f.close()
            except IOError as xxxTodoChangeme:
                (errno, strerror) = xxxTodoChangeme.args
                print("IOError [{0}]: {1}".format(errno, strerror))
                # TODO: error codes
                return None
                
            return data
        else:
            # TODO: error codes
            print("could not access: " + directory)
            return None

    def editField(self, parent, generateDir, field, data):
        """writes the field string into the proper directory.

        Note that this function will overwrite any previous data! Be
        sure to provide the new data in totality so you don't lose
        anything."""
        directory = generateDir(parent)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/" + field + ".txt", "w")
                f.write(data)
                f.close()
            except IOError as error:
                (errno, sterror) = error
                print("IOError [{0}]: {1}".format(errno, strerror))
                raise error

    def editPatientNotes(self, patient):
        self.editField(patient, self.generatePatientDir, "notes", patient.notes)

    def editPatientPhysicians(self, patient):
        self.editField(patient, self.generatePatientDir, "physicians", "\n".join(map(str, patient.physicians)))

    def editPhotosetTreatments(self, photoset):
        self.editField(photoset, self.generatePhotosetDir, "treatments", "\n".join(map(str, photoset.treatments)))

    def editPhotosetDiagnoses(self, photoset):
        self.editField(photoset, self.generatePhotosetDir, "diagnoses", "\n".join(map(str, photoset.diagnoses)))

    def loadPatientNotes(self, patient):
        return self.getPatientDataFromField(patient, "notes.txt")

    def loadPatientPhysicians(self, patient):
        data = self.getPatientDataFromField(patient, "physicians.txt")
        physicians = list()
        if data is None:
            # TODO error?
            return None
        else:
            data = self.parseNames(data)
            for i in data:
                pass
                #d = Physician()
                #d.firstName, d.lastName, d.uid = int(i)
                #physicians.append(d)
                #patient.physicians.append( d )
                #print patient.physicians
            return physicians
    
    def loadPatientPhotosetList(self, patient):
        # not done
        if self.isNew():
            return None

        directory = self.generatePatientDir(patient)
        if os.path.isdir(directory):
            try:
                items = os.listdir(directory)
                for i in items:
                    if os.path.isdir(directory + "/" + i):
                        splitName = i.split("#")
                        uid = splitName[1]
                        date = splitName[0].split("-")
                        d = datetime.date(int(date[2]), int(date[1]), int(date[0])) # year, month, day

                        p = photoset.Photoset(patientinit=patient, dateinit=d)
                        p.dm = patient.dm
                        p.uid = int(uid)

                        patient.photosets |= set([p])
            except IOError as xxxTodoChangeme1:
                (errno, strerror) = xxxTodoChangeme1.args
                print("IOError [{0}]: {1}".format(errno, strerror))

    def loadPhotosetTags(self, photoset):
        if self.isNew():
            # TODO: error codes
            return None

        directory = self.generatePhotosetDir(photoset, photoset.patient)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/diagnoses.txt")
                data = f.read()
                f.close()
            except IOError as xxxTodoChangeme2:
                (errno, strerror) = xxxTodoChangeme2.args
                print("IOError [{0}]: {1}".format(errno, strerror))
                # TODO: error codes
                return None
                
            try:
                f = open(directory + "/treatments.txt")
                data = data + "\n" + f.read()
                f.close()
            except IOError as xxxTodoChangeme3:
                (errno, strerror) = xxxTodoChangeme3.args
                print("IOError [{0}]: {1}".format(errno, strerror))
                # TODO: error codes
                return None

            data = data.splitlines()
            return data
        else:
            # TODO: error codes
            print("could not access: " + directory) 
            return None

    def loadPhotosetDiagnoses(self, photoset):
        if self.isNew():
            # TODO: error codes
            return None

        directory = self.generatePhotosetDir(photoset)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/diagnoses.txt")
                data = f.read()
                f.close()
            except IOError as xxxTodoChangeme4:
                (errno, strerror) = xxxTodoChangeme4.args
                print("IOError [{0}]: {1}".format(errno, strerror))
                # TODO: error codes
                return None

            data = data.splitlines()
            return data
        else:
            # TODO: error codes
            print("could not access: " + directory) 
            return None

    def loadPhotosetTreatments(self, photoset):
        if self.isNew():
            # TODO: error codes
            return None

        directory = self.generatePhotosetDir(photoset)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/treatments.txt")
                data = f.read()
                f.close()
            except IOError as xxxTodoChangeme5:
                (errno, strerror) = xxxTodoChangeme5.args
                print("IOError [{0}]: {1}".format(errno, strerror))
                # TODO: error codes
                return None

            data = data.splitlines()
            return data
        else:
            # TODO: error codes
            print("could not access: " + directory) 
            return None
