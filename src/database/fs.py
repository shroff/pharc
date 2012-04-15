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

        self.patientUID = 0
        self.photosetUID = 70000
        self.knownPatientUIDs = False
        self.knownPhotosetUIDs = False
        return

    # Cleanup/validation before program termination
    def exit(self):
        return

    # this will be very slow... should probably be spun off on its own after loadAllPatients()
    def discoverPhotosetUIDs(self):
        items = os.listdir(self.root)
        for i in items:
            directory = self.root + "/" + i
            if os.path.isdir(directory):
                photosets = os.listdir(directory)
                for j in photosets:
                    photosetDirectory = directory + "/" + j
                    if os.path.isdir(photosetDirectory):
                        uid = int(j.split("#")[1])
                        if uid > photosetUID:
                            photosetUID = uid

    # Returns if the data storage existed prior to class init
    def isNew(self):
        return self.newFS

    def makeFile(self, path, data=''):
        f = open(path, 'w')
        f.write(data)
        f.close()

    def createPatient(self, firstName, lastName):
        if not self.isNew():
            if not self.knownPatientUIDs():
                # if you see this, then you did not call loadAllPatients() on program startup
                raise Exception
            uid = self.patientUID + 1
        else:
            uid = self.patientUID


        p = patient.Patient()
        p.firstName = firstName
        p.lastName = lastName
        p.uid = uid

        directory = self.generatePatientDir(p)

        shutil.makedirs(directory)
        self.makeFile(directory + "/name.txt", firstName + ", " + lastName + "#" + str(uid))
        self.makeFile(directory + "/physicians.txt")
        self.makeFile(directory + "/notes.txt")

        self.newFS = False

    def createPhotoset(self, photoset, patient):
        if not self.knownPhotosetUIDs:
            self.discoverPhotosetUIDs()

        uid = self.photosetUID
        uid = uid + 1
        photoset.uid = uid

        directory = generatePhotosetDir(photoset, patient)
        os.makedirs(directory)
        self.makeFile(directory + "/physicians.txt")
        self.makeFile(directory + "/notes.txt")
        self.makeFile(directory + "/treatments.txt")
        self.makeFile(directory + "/diagnoses.txt")

        self.photosetUID = uid

    def copyPhotoset(self, photoset, toPatient):
        fromDirectory = self.generatePhotosetDir(photoset)
        toDirectory = self.generatePhotosetDir(photoset, photoset.toPatient)

        if not os.path.isdir(fromDirectory):
            return
        if os.path.isdir(toDirectory):
            # We have a database inconsistency, how should we handle it?
            # For now, die.
            raise Exception

        shutil.copytree(fromDirectory, toDirectory)


    def deletePhotoset(self, photoset):
        # How do we handle UIDs?
        directory = self.generatePhotosetDir(photoset)
        shutil.rmtree(directory)

    # Returns a list of all the patients
    def loadAllPatients(self):
        patients = []

        items = os.listdir(self.root)
        for i in items:
            if os.path.isdir(self.root + "/" + i):
                p = patient.Patient()
                # Parse filename
                p.nameFirst, p.nameLast, p.uid = self.parseName(i)
                p.uid = int(p.uid)
                if p.uid > self.patientUID:
                    self.patientUID = p.uid
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

    def generatePhotosetDir(self, photoset, patient=None):
        if patient is None:
            patient = photoset.patient

        directory = self.generatePatientDir(patient)
        uid = str(photoset.uid)
        date = photoset.date
        if os.path.isdir(directory):
            return directory + "/" + str(date.day).zfill(2) + "-" + str(date.month).zfill(2) + \
                "-" + str(date.year) + "#" + uid
        

    def getPatientDataFromField(self, patient, field):
        directory = self.generatePatientDir(patient)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/" + field)
                data = f.read()
                f.close()
            except IOError as error:
                (errno, strerror) = error.args
                print("IOError [{0}]: {1}".format(errno, strerror))
                # TODO: error codes
                return None
                
            return data
        else:
            # TODO: error codes
            print("could not access: " + directory)
            return None

    def editField(self, parent, generateDir, field, data):
        directory = generateDir(parent)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/" + field + ".txt")
                #f.write(data)
                #f.close()
            except IOError as error:
                print error
                raise error

    def editPatientNotes(self, patient, notes):
        self.editField(patient, self.generatePatientDir, "notes", notes)

    def editPatientPhysicians(self, patient, physicians):
        self.editField(patient, self.generatePatientDir, "physicians", physicians)

    def editPhotosetTreatments(self, photoset, treatments):
        self.editField(photoset, self.generatePhotosetDir, "treatments", treatments)

    def editPhotosetDiagnoses(self, photoset, diagnoses):
        self.editField(photoset, self.generatePhotosetDir, "diagnoses", diagnoses)

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
            return physicians
    
    def loadPatientPhotosetList(self, patient):
        directory = self.generatePatientDir(patient)
        if os.path.isdir(directory):
            try:
                items = os.listdir(directory)
                for i in items:
                    if os.path.isdir(directory + "/" + i):
                        splitName = i.split("#")
                        uid = splitName[1]

                        date = splitName[0].split("-")
                        date = datetime.date(int(date[2]), int(date[1]), int(date[0])) # year, month, day

                        p = photoset.Photoset(patientinit=patient, dateinit=date)
                        p.dm = patient.dm
                        p.uid = int(uid)

                        # determine date
                        patient.photosets |= set([p])

            except IOError as error:
                (errno, strerror) = error.args
                print("IOError [{0}]: {1}".format(errno, strerror))

    def loadPhotosetTags(self, photoset):
        directory = self.generatePhotosetDir(photoset)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/diagnoses.txt")
                data = f.read()
                f.close()
            except IOError as error:
                (errno, strerror) = error.args
                print("IOError [{0}]: {1}".format(errno, strerror))
                # TODO: error codes
                return None
                
            try:
                f = open(directory + "/treatments.txt")
                data = data + "\n" + f.read()
                f.close()
            except IOError as error:
                (errno, strerror) = error.args
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
        directory = self.generatePhotosetDir(photoset)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/diagnoses.txt")
                data = f.read()
                f.close()
            except IOError as error:
                (errno, strerror) = error.args
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
        directory = self.generatePhotosetDir(photoset)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/treatments.txt")
                data = f.read()
                f.close()
            except IOError as error:
                (errno, strerror) = error.args
                print("IOError [{0}]: {1}".format(errno, strerror))
                # TODO: error codes
                return None

            data = data.splitlines()
            return data
        else:
            # TODO: error codes
            print("could not access: " + directory) 
            return None
