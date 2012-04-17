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

validImageTypes = frozenset([ \
    "GIF", \
    "JPG", \
    "JPEG", \
    "PNG", \
    "TIFF"
    ])

import os, sys, datetime, shutil

import logic.patient as patient
import logic.photoset as photoset
import logic.photo as photo

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
        """
            Determines the highest Photoset UID in the database so that we
            can continue generating unique IDs for new photosets.

            Arguments:
                N/A

            Returns:
                N/A -- Sets self.photosetUID

            Throws:
                ?
        """
        items = os.listdir(self.root)
        for i in items:
            directory = self.root + "/" + i
            if os.path.isdir(directory):
                photosets = os.listdir(directory)
                for j in photosets:
                    photosetDirectory = directory + "/" + j
                    if os.path.isdir(photosetDirectory):
                        uid = int(j.split("#")[1])
                        if uid > self.photosetUID:
                            self.photosetUID = uid

    # Returns if the data storage existed prior to class init
    def isNew(self):
        """
            Returns whether or not the database was newly created.

            Used for short-circuting certain operations that don't make
            sense on an empty database, as well as creating new parts of it.

            Arguments:
                N/A

            Returns:
                True if the database did not exist, False otherwise.

            Throws:
                N/A
        """
        return self.newFS

    def makeFile(self, path, data=''):
        """
            Handles writing data to a file in one location.

            Arguments:
                path: The location to write to.
                data: The data to write to path.

            Returns:
                N/A

            Throws:
                ?
        """
        f = open(path, 'w')
        f.write(data)
        f.close()

    def createPatient(self, firstName, lastName):
        """
            Create a new patient.

            Arguments:
                firstName: A string for the first name of the patient.
                lastName:  A string for the last name of the patient.

            Returns:
                N/A

            Throws:
                IOError
                Error
        """
        if not self.isNew():
            if not self.knownPatientUIDs:
                # if you see this, then you did not call loadAllPatients() on program startup
                raise Exception
            uid = self.patientUID + 1
        else:
            uid = self.patientUID


        p = patient.Patient(fname=firstName, lname=lastName, num=uid)

        directory = self.generatePatientDir(p)

        os.makedirs(directory)
        self.makeFile(directory + "/name.txt", firstName + ", " + lastName + "#" + str(uid))
        self.makeFile(directory + "/physicians.txt")
        self.makeFile(directory + "/notes.txt")

        self.newFS = False
        
        return p

    def createPhotoset(self, patientinit, dateinit):
        """
            Create a new photoset.

            Arguments:
                photoset: The photoset object we want to save.
                patientinit:  The patient who owns this photoset.

            Returns:
                N/A

            Throws:
                IOError
                Error
        """
        if not self.knownPhotosetUIDs:
            self.discoverPhotosetUIDs()

        if dateinit is None:
            dateinit = datetime.date.today()

        ps = photoset.Photoset(dateinit, patientinit)

        uid = self.photosetUID
        uid = uid + 1
        ps.uid = uid

        directory = self.generatePatientDir(patientinit)
        directory = directory + "/" + str(dateinit.day).zfill(2) + "-" + str(dateinit.month).zfill(2) + \
            "-" + str(dateinit.year) + "#" + str(uid)

        os.makedirs(directory)
        self.makeFile(directory + "/physicians.txt")
        self.makeFile(directory + "/notes.txt")
        self.makeFile(directory + "/treatments.txt")
        self.makeFile(directory + "/diagnoses.txt")

        self.photosetUID = uid

        return ps

    def copyPhotoset(self, photoset, fromDirectory, toDirectory):
        """
            Move a new photoset to a different patient.

            Arguments:
                photoset:      The photoset object we want to save.
                fromDirectory: The directory the photoset currently exists at.
                toDirectory:   The directory to move the photoset to.

            Returns:
                N/A

            Throws:
                Error
                Exception
        """
        if not os.path.isdir(fromDirectory):
            return
        if os.path.isdir(toDirectory):
            # We have a database inconsistency, how should we handle it?
            # For now, die.
            raise Exception

        shutil.copytree(fromDirectory, toDirectory)


    def deletePhotoset(self, photoset):
        """
            Delete a photoset.

            Arguments:
                photoset: The photoset object we want to save.

            Returns:
                N/A

            Throws:
                Error
                OSError
        """
        # How do we handle UIDs?
        directory = self.generatePhotosetDir(photoset)
        shutil.rmtree(directory)

    # Returns a list of all the patients
    def loadAllPatients(self):
        """
            Load a list of all the patients in the database.

            Arguments:
                N/A

            Returns:
                A list of Patients.

            Throws:
                ?
        """
        patients = []

        items = os.listdir(self.root)
        for i in items:
            if os.path.isdir(self.root + "/" + i):
                nameFirst, nameLast, uid = self.parseName(i)
                p = patient.Patient(fname=nameFirst, lname=nameLast, num=uid)
                # Parse filename
                p.uid = int(p.uid)
                if p.uid > self.patientUID:
                    self.patientUID = p.uid
                patients.append(p)

        self.knownPatientUIDs = True
        return patients

    def parseName(self, name):
        """
            Parse a name per our format specifications:

            firstName, lastName#UID

            Arguments:
                name: The string to parse.

            Returns:
                tuple:
                    firstName
                    lastName
                    UID

            Throws:
                ?
        """
        unparsedName = name.split('#')[0]
        unparsedName = unparsedName.split()
        nameFirst = unparsedName[1]
        nameLast = unparsedName[0][:-1]
        uid = int(name.split('#')[1])

        return [nameFirst, nameLast, uid]

    def parseNames(self, names):
        """
            Parse a list of names in a line delimited string.

            Arguments:
                names: A string of names, per format specs, separated by newlines.

            Returns:
                A list of parsed name tuples generated by parseName()

            Throws:
                ?
        """
        unparsedNameList = names.split('\n')
        parsedNameList = []
        for i in unparsedNameList:
            parsedNameList.append( self.parseName(i) )

        return parsedNameList

    def generatePatientDir(self, patient):
        """
            Generate the string representation of the path for the directory of
            this patient.

            Arguments:
                patient: The patient we want the directory for.

            Returns:
                String representation of the path for this patient's directory.

            Throws:
                ?
        """
        return self.root + "/" + patient.nameLast + ", " + patient.nameFirst + "#" + str(patient.uid)

    def generatePhotosetDir(self, photoset, patient=None):
        """
            Generate the string representation of the path for the directory of
            this photoset.

            Arguments:
                photoset: The photoset we want the directory for.
                patient:  The patient who owns/should own this photoset.
                          If None, assume photoset.patient.

            Returns:
                String representation of the path for this photoset's directory.

            Throws:
                ?
        """
        if patient is None:
            patient = photoset.patient

        directory = self.generatePatientDir(patient)
        uid = str(photoset.uid)
        date = photoset.date
        if os.path.isdir(directory):
            return directory + "/" + str(date.day).zfill(2) + "-" + str(date.month).zfill(2) + \
                "-" + str(date.year) + "#" + uid
        

    def getPatientDataFromField(self, patient, field):
        """
            Return the data for a field of a patient in the database.

            Arguments:
                patient: The patient in question.
                field:   The name of the field we want the data from.

            Returns:
                The data from the field or None, if none was found.

            Throws:
                ?
        """
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
        """
            Modify a given field of a photoset or patient.

            Arguments:
                parent:      Either a photoset or a patient.
                generateDir: The function to generate the directory for the parent
                             object, e.g. generatePatientDir for a Patient.
                field:       The name of the field to modify, e.g. notes.
                data:        The data to store in the field, is not appended.

            Returns:
                N/A

            Throws:
                IOError
        """
        directory = generateDir(parent)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/" + field + ".txt", 'w')
                f.write(data)
                f.close()
            except IOError as error:
                print(error)
                raise error

    def editPatientNotes(self, patient, notes):
        """
            Wrapper for editField() for editing the patient notes field.

            Arguments:
                patient: The patient who's notes we wish to change.
                notes:   The actual notes we wish to save.

            Returns:
                N/A

            Throws:
                IOError
        """
        self.editField(patient, self.generatePatientDir, "notes", notes)

    def editPatientPhysicians(self, patient, physicians):
        """
            Wrapper for editField() for editing the patient physicians field.

            Arguments:
                patient:    The patient who's notes we wish to change.
                physicians: The actual string representation of the physicians list
                            we wish to save.

            Returns:
                N/A

            Throws:
                IOError
        """
        self.editField(patient, self.generatePatientDir, "physicians", physicians)

    def editPhotosetTreatments(self, photoset, treatments):
        """
            Wrapper for editField() for editing the photoset treatments field.

            Arguments:
                photoset:   The photoset who's notes we wish to change.
                treatments: The actual string representation of the treatments
                            list we wish to save.

            Returns:
                N/A

            Throws:
                IOError
        """
        self.editField(photoset, self.generatePhotosetDir, "treatments", treatments)

    def editPhotosetDiagnoses(self, photoset, diagnoses):
        """
            Wrapper for editField() for editing the photoset diagnoses field.

            Arguments:
                photoset:  The photoset who's notes we wish to change.
                diagnoses: The actual string representation of the diagnoses
                           list we wish to save.

            Returns:
                N/A

            Throws:
                IOError
        """
        self.editField(photoset, self.generatePhotosetDir, "diagnoses", diagnoses)

    def loadPatientNotes(self, patient):
        """
            Wrapper for getPatientDataFromField which loads the notes field's data.

            Arguments:
                patient: The patient who's notes we want.

            Returns:
                String representation of the notes field.

            Throws:
                IOError
        """
        return self.getPatientDataFromField(patient, "notes.txt")

    def loadPatientPhysicians(self, patient):
        """
            Wrapper for getPatientDataFromField which loads the physicians' data.
            Parses the data into tuples for easy processing later.

            Arguments:
                patient: The patient who's physicians we want.

            Returns:
                Tuple representation of the physicians field, parsed by parseNames()
                None if no physicians.
            
            Throws:
                IOError
        """
        data = self.getPatientDataFromField(patient, "physicians.txt")
        physicians = list()
        if data is None:
            # TODO error?
            return None
        else:
            data = self.parseNames(data)
            return physicians
    
    def loadPatientPhotosetList(self, patient):
        """
            Loads a patient's list of photosets.

            Arguments:
                patient: The patient who's photoset list we want.

            Returns:
                N/A -- Fills the photoset list field in patient
            
            Throws:
                IOError
        """
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
                raise error

    def loadPhotosetTags(self, photoset):
        """
            Loads the tags for a photoset. Collated from diagnoses.txt and
            treatments.txt.

            Arguments:
                photoset: The photoset who's tag list we want.

            Returns:
                A list of tag strings.
            
            Throws:
                IOError
        """
        directory = self.generatePhotosetDir(photoset)
        if os.path.isdir(directory):
            try:
                f = open(directory + "/diagnoses.txt")
                data = f.read()
                f.close()
            except IOError as error:
                (errno, strerror) = error.args
                print("IOError [{0}]: {1}".format(errno, strerror))
                
            try:
                f = open(directory + "/treatments.txt")
                data = data + "\n" + f.read()
                f.close()
            except IOError as error:
                (errno, strerror) = error.args
                print("IOError [{0}]: {1}".format(errno, strerror))

            data = data.splitlines()
            return data
        else:
            # TODO: error codes
            print("could not access: " + directory) 
            return None

    def loadPhotosetDiagnoses(self, photoset):
        """
            Loads the diagnoses for a photoset. 

            Arguments:
                photoset: The photoset who's tag list we want.

            Returns:
                A list of tag strings.
            
            Throws:
                IOError
        """
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
        """
            Loads the treatments for a photoset. 

            Arguments:
                photoset: The photoset who's tag list we want.

            Returns:
                A list of tag strings.
            
            Throws:
                IOError
        """
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

    def loadPhoto(self, photo):
        """
            Loads the actual photo.

            Arguments:
                photo: The photo object who's data we want.

            Returns:
                The image data for the photo.

            Throws:
                IOError
                ?
        """
        directory = self.generatePhotosetDir(photo.photoset)
        if os.path.isdir(directory):
            data = directory + "/" + photo.name
            return data

    def renamePatient(self, patient, firstName, lastName):
        """
            Moves a patient that we want to rename in the filesystem.

            Arguments:
                patient:   The patient whom we wish to move.
                firstName: The new first name of the patient.
                lastName:  The new last name of the patient.

            Returns:
                N/A

            Throws:
                Error
                ?
        """
        uid = patient.uid
        fromDirectory = self.generatePatientDir(patient)
        toDirectory = self.root + "/" + lastName + ", " + firstName + "#" + str(uid)

        if not os.path.isdir(fromDirectory):
            raise Exception

        shutil.copytree(fromDirectory, toDirectory)

        shutil.rmtree(fromDirectory)


    def renamePhoto(self, photo, name):
        """
            Renames a photo in the filesystem.

            Arguments:
                photo: The photo object we want to rename.
                name:  The new name.

            Returns:
                N/A

            Throws:
                Error
        """
        directory = self.generatePhotosetDir(photo.photoset)
        fromPath = directory + "/" + photo.name
        if os.path.isdir(directory):
            shutil.copy(fromPath, directory + "/" + name)
            shutil.rmtree(fromPath)


    def movePhoto(self, photo, photoset):
        """
            Moves a photo from one photoset to another.

            Arguments:
                photo:      The photo object we want to move.
                toPhotoset: The photoset we want to move the photo to.

            Returns:
                N/A

            Throws:
                ?
        """
        name = photo.name
        fromPath = self.generatePhotosetDir(photo.photoset) + "/" + name
        toPath = self.generatePhotosetDir(photoset) + "/" + name

        shutil.copy(fromPath, toPath)
        shutil.rmtree(toPath)

    def loadPhotosetPhotos(self, photoset):
        """
            Load's a given photoset's photos

            Arguments:
                photoset: The photoset who's photos we want to load.

            Returns:
                The list of photos.

            Throws:
                ?
        """
        photos = []

        directory = self.generatePhotosetDir(photoset)
        items = os.listdir(directory)
        for i in items:
            if self.isImage(i):
                photos.append( photo.Photo(i, photoset))
        return photos

    def isImage(self, name):
        """
            Verifies that a given filename has a valid extension.

            Arguments:
                name: The filename in question.

            Returns:
                True if the extension is valid, False otherwise.

            Throws:
                N/A
        """
        ext = name.split('.')[1].upper()

        if ext not in validImageTypes:
            return False
        return True
        
    def importPhoto(self, path, photoset):
        """
            Moves a given file into a photoset's directory.

            Arguments:
                path:     The path to the file we want to move.
                photoset: The photoset we want to own this file.

            Returns:
                N/A

            Throws:
                ?
        """
        directory = self.generatePhotosetDir(photoset)

        if os.path.isdir(directory):
            shutil.move(path, directory)

    def findPhotos(self, path):
        images = []

        if not os.path.isdir(path):
            return images
        for i in os.listdir(path):
            print (i)
            if i.split('.')[1].upper() in validImageTypes:
                images.append(i)

        return images

