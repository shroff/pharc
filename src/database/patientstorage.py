# PHARC: a photo archiving application for physicians
# Copyright (C) 2012  Saul Reynolds-Haertle
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

class PatientStorage(object):

    def __init__(self, fsm):
        """
            Initialize a PatientStorage object.

            Arguments:
                fsm: Reference to a FS object.
        """
        # there may be a better way of handling this, but it should do
        self.fsm = fsm

    def loadField(self, patient, fm):
        """
            Loads a field for a Patient, e.g. notes, physicians.

            Arguments:
                patient: The patient who's field we want to load.
                fm:      The FS method to call.

            Returns:
                The data from the field that was loaded.

            Throws:
                ?
        """
        data = fm(patient)

        return data


    def loadNotes(self, patient):
        """
            Wrapper for loading notes using loadField().

            Arguments:
                patient: The patient who's notes we want.

            Returns:
                N/A -- Sets the notes field of patient directly

            Throws:
                ?
        """
        notes = self.fsm.loadPatientNotes(patient)
        if notes is None:
            return
        else:
            patient.notes = notes
            return

    def checkNewFS(self):
        """
            Determines whether or not the filesystem is brand new.
            
            Arguments:
                N/A

            Returns:
                True if the filesystem is newly made, False otherwise.

            Throws:
                N/A
        """
        return self.fsm.isNew()

    def loadPhysicians(self, patient):
        """
            Load the physicians list for a patient.

            Arguments:
                patient: The patient who's physicians we want.

            Returns:
                N/A -- sets the physicians field directly

            Throws:
                ?
        """
        if not self.checkNewFS():
            patient.physicians = self.loadField(patient, self.fsm.loadPatientPhysicians, None)

    def loadPhotosets(self, patient):
        """
            Load the list of photosets for a patient.

            Arguments:
                patient: The patient who's photosets we want.

            Returns:
                N/A -- sets the photosets list directly

            Throws:
                ?
        """
        if not self.checkNewFS():
            self.fsm.loadPatientPhotosetList(patient)

    def createPatient(self, firstName, lastName, physicians=""):
        """
            Creates a new patient.

            Arguments:
                firstName:  The first name of the patient.
                lastName:   The last name of the patient.
                physicians: A list of the physicians who own this patient.

            Returns:
                A new patient object.

            Throws:
                ?
        """
        patient = self.fsm.createPatient(firstName, lastName)
        self.fsm.editPatientPhysicians(patient, physicians)
        return patient

    def editName(self, patient, firstName, lastName):
        """
            Changes the name of a patient and adjusts it's database entries.

            Arguments:
                patient:   The patient whom we wish to rename.
                firstName: The first name of the patient.
                lastName:  The last name of the patient.

            Returns:
                N/A

            Throws:
                ?
        """
        if not self.checkNewFS():
            self.fsm.renamePatient(patient, firstName, lastName) 

    def editPhysicians(self, patient, physicians):
        """
            Changes the physician list in the database for the patient.

            Arguments:
                patient:    The patient who's physicians we want to change.
                physicians: The new list of physicians.

            Returns:
                N/A

            Throws:
                ?
        """
        if not self.checkNewFS():
            self.fsm.editPatientPhysicians(patient, physicians)

    def editNotes(self, patient, notes):
        """
            Changes the notes in the database for the patient.

            Arguments:
                patient: The patient who's notes we want to change.
                notes:   The new notes for the patient.

            Returns:
                N/A

            Throws:
                ?
        """
        if not self.checkNewFS():
            self.fsm.editPatientNotes(patient, notes)

    def loadAllPatients(self):
        """
            Loads a list of all of the patients in the database.

            Arguments:
                N/A

            Returns:
                The list of patients in the database.

            Throws:
                ?
        """
        if not self.checkNewFS():
            return self.fsm.loadAllPatients()
