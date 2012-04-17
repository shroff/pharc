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

import database.fs
from logic.datamanager import DataManager
from .importpatientphotos import ImportPatientPhotos
from .patientsearch import PatientSearch
from .photosetadd import PhotosetAdd

class ImportPage(QWidget):
  def __init__(self, parent, dm, pList):
    super(ImportPage, self).__init__(parent)
    self.parent = parent
    self.data = dm
    self.currPatientList = pList

    self.initUI()

  def initUI(self):
    vboxMain = QVBoxLayout()
    hboxMain = QHBoxLayout()
    hboxButtons = QHBoxLayout()
    vboxInfo = QVBoxLayout()

    addButton = QPushButton("Add")
    skipButton = QPushButton("Do this later")
    self.connect(skipButton, SIGNAL("clicked()"), self.parent.viewMain)
    hboxButtons.addStretch(1)
    hboxButtons.addWidget(addButton)
    hboxButtons.addWidget(skipButton)

    self.photoScrollArea = QScrollArea()
    self.photos = ImportPatientPhotos(self)
    self.photoScrollArea.setWidget(self.photos)
    self.photoScrollArea.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
    self.photoScrollArea.setBackgroundRole(QPalette.Light)

    self.patientSearch = PatientSearch(self, self.data, self.currPatientList)
    self.photosetAdd = PhotosetAdd(self, self.data)
    vboxInfo.addWidget(self.patientSearch)
    vboxInfo.addWidget(self.photosetAdd)

    hboxMain.addWidget(self.photoScrollArea)
    hboxMain.addLayout(vboxInfo)
    vboxMain.addLayout(hboxMain)
    vboxMain.addLayout(hboxButtons)

    self.setLayout(vboxMain)

  def select(self, patient):
    self.photosetAdd.setPatient(patient)

  def triggerUpdate(self):
    self.parent.triggerUpdate()

  def modelUpdated(self):
    self.patientSearch.modelUpdated()
