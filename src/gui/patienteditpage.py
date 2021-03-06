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
from PyQt4.QtCore import *

from .patientphotos import PatientPhotos
from .patientnamerow import PatientNameRow
from .patientdetailtable import PatientDetailTable

import database.fs
from logic.datamanager import DataManager

class PatientEditPage(QWidget):
  def __init__(self, parent, dm):
    super(PatientEditPage, self).__init__(parent)
    self.dataManager = dm
    self.parent = parent
    self.initUI()
    self.patient = None

  def initUI(self):
    vbox = QVBoxLayout()
    self.nameRow = PatientNameRow()
    self.detailTable = PatientDetailTable(self, self.dataManager)
    vbox.addWidget(self.nameRow)
    vbox.addWidget(self.detailTable)

    self.photo = PatientPhotos(self, self.dataManager, horiz=True)
    self.photo.setVisible(False)
    vbox.addWidget(self.photo)

    self.save = QPushButton('Save Changes')
    self.cancel = QPushButton('Return')

    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(self.save)
    hbox.addWidget(self.cancel)

    vbox.addLayout(hbox)

    QObject.connect(self.save, SIGNAL('clicked()'), self.saveChanges)
    QObject.connect(self.cancel, SIGNAL('clicked()'), self.cancelChanges)

    self.setLayout(vbox)

  def saveChanges(self):
    self.nameRow.savePatient()
    print('Saving')
    for edit in self.detailTable.queuededits:
      (ps, field) = edit
      val = self.detailTable.queuededits[edit]
      if field == 'date':
        ps.date = val
      if field == 'diagnosis':
        ps.clearDiagnoses()
        ps.addDiagnoses(val)
      if field == 'treatment':
        ps.clearTreatments()
        ps.addTreatments(val)
    self.detailTable.queuededits = {}
    self.parent.triggerUpdate()

  def cancelChanges(self):
    self.detailTable.queuededits = {}
    self.parent.viewMain()

  def selected(self, ps):
    self.photo.setSelected(self.parent.selected)
    self.photo.refresh(ps.photos, self.dataManager.loader.PhotosetStorage.getPath(ps))
    self.photo.setVisible(True)

  def setPatient(self, patient):
    self.patient = patient
    self.nameRow.setPatient(self.patient)
    self.detailTable.setPatient(self.patient)
    self.photo.setVisible(False)

  def toggle(self, path):
    self.parent.toggle(path)

  def clearSelection(self):
    if(self.patient != None):
      self.setPatient(self.patient)

