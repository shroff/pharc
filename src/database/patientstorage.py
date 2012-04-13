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

    def __init__(self, dbm, fsm):
        # there may be a better way of handling this, but it should do
        self.dbm = dbm
        self.fsm = fsm

    def loadField(self, patient, fm, dm):
        #TODO database loading

        data = fm(patient)
        #TODO error handling

        return data


    def loadNotes(self, patient):
        #TODO try database before filesystem

        notes = self.fsm.loadPatientNotes(patient)
        if notes is None:
            # TODO Error code
            return
        else:
            patient.notes = notes
            # TODO Success code
            return

    def loadPhysicians(self, patient):
        patient.physicians = self.loadField(patient, self.fsm.loadPatientPhysicians, None)

    def loadPhotosets(self, patient):
        self.fsm.loadPatientPhotosetList(patient)

    def createPatient(self, firstName, lastName, physicians):
        patient = self.fsm.addPatient(firstName, lastName)
        self.fsm.addPhysicians(patient, physicians)
        return patient

    def editName(self, firstName, lastName):
        pass

    def editPhysicians(self, patient, physicians):
        self.fsm.editPatientPhysicians(patient, physicians)

    def editNotes(self, patient, notes):
        self.fsm.editPatientNotes(patient, notes)

    def loadAllPatients(self):
        return self.fsm.loadAllPatients()
