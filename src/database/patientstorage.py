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

from . import db
from . import fs

# import sys
# sys.path.append('../logic')
from logic.patient import Patient

class PatientStorage:

    def __init__(self, dbm, fsm):
        # there may be a better way of handling this, but it should do
        self.dbm = dbm
        self.fsm = fsm

    def load_field(self, patient, fm, dm):
        #TODO database loading

        data = fm(patient)
        #TODO error handling

        return data


    def load_notes(self, patient):
        #TODO try database before filesystem

        notes = self.fsm.load_patient_notes(patient)
        if notes is None:
            # TODO Error code
            return
        else:
            patient.notes = notes
            # TODO Success code
            return

    def load_physicians(self, patient):
        patient.physicians = self.load_field(patient, self.fsm.load_patient_physicians, None)

    def load_photosets(self, patient):
        self.fsm.load_patient_photoset_list(patient)

    def create_patient(self, first_name, last_name, physicians):
        patient = self.fsm.add_patient(first_name, last_name)
        self.fsm.add_physicians(patient, physicians)
        return patient

    def edit_name(self, first_name, last_name):
        pass

    def edit_physicians(self, patient, physicians):
        pass

    def edit_notes(self, patient, notes):
        pass

    def load_all_patients(self):
        pass
