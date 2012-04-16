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
  def __init__(self, parent, dm):
    self.data = dm
    super(PatientInfo, self).__init__(parent)
    self.parent = parent
    self.initUI()
    self.index = 0


  def initUI(self):
    hbox = QHBoxLayout()
    self.patientTable = PatientTable(self, self.data)
    self.patientDetail = PatientDetail(self)
    self.patientDetail.setVisible(False)
    hbox.addWidget(self.patientTable)
    hbox.addWidget(self.patientDetail)

    self.setLayout(hbox)


  def viewInfo(self, row, col):
    patient = self.data.patients[row]
    self.patientDetail.setName(patient.nameFirst + " " + patient.nameLast)
    ps = patient.getMostRecentPhotoset()
    self.patientDetail.setTreatment(" ".join(map(str, ps.treatments)))
    self.patientDetail.setDiagnosis(" ".join(map(str, ps.diagnoses)))
    self.patientDetail.setRandom()
    self.patientDetail.setVisible(True)
    self.index = row

  def viewDetails(self):
    if(self.patientDetail.isVisible()):
      self.parent.viewDetails(self.index)

  def update(self):
    self.patientDetail.setVisible(False)
    self.patientTable.update()
