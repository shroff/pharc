# PHARC: a photo archiving application for physicians
# Copyright (C) 2012 Abhishek Shroff
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

from PyQt4.QtGui import *

from .patienttable import PatientTable
from .patientdetail import PatientDetail

import database.fs
from logic.datamanager import DataManager
from logic.patient import Patient

#data = None

class PatientInfo(QWidget):
  def __init__(self, parent, dm, pList):
    self.data = dm
    super(PatientInfo, self).__init__(parent)
    self.parent = parent
    self.currPatientList = pList
    self.initUI()
    self.patient = None


  def initUI(self):
    hbox = QHBoxLayout()
    self.patientTable = PatientTable(self, self.data, self.currPatientList)
    self.patientDetail = PatientDetail(self)
    self.patientDetail.setVisible(False)
    hbox.addWidget(self.patientTable)
    hbox.addWidget(self.patientDetail)

    self.setLayout(hbox)


  def select(self, patient):
    self.patient = patient
    self.patientDetail.setName(patient.nameFirst + " " + patient.nameLast)
    ps = patient.getMostRecentPhotoset()
    self.patientDetail.setTreatment(", ".join(map(str, patient.treatments)))
    self.patientDetail.setDiagnosis(", ".join(map(str, patient.diagnoses)))
    self.patientDetail.setPicture(ps.photos[0].getData())
    self.patientDetail.setVisible(True)

  def viewDetails(self):
    if(self.patientDetail.isVisible()):
      self.parent.viewDetails(self.patient)

  def updateSearch(self, pats):
    self.patientDetail.setVisible(False)
    self.currPatientList = pats
    self.patientTable.updateSearch(pats)

  def update(self):
    self.patientDetail.setVisible(False)
    self.patientTable.update()
