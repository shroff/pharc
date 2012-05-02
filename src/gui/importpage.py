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
from .patientphotos import PatientPhotos
from .patientsearch import PatientSearch
from .photosetadd import PhotosetAdd

imageBase = "import/"

class ImportPage(QWidget):
  def __init__(self, parent, dm, pList):
    super(ImportPage, self).__init__(parent)
    self.parent = parent
    self.dataManager = dm
    self.currPatientList = pList
    self.selected = set()

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

    self.photo = PatientPhotos(self, self.dataManager)

    self.patientSearch = PatientSearch(self, self.dataManager, self.currPatientList)
    self.photosetAdd = PhotosetAdd(self, self.dataManager)
    vboxInfo.addWidget(self.patientSearch)
    vboxInfo.addWidget(self.photosetAdd)

    hboxMain.addWidget(self.photo)
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

  def add(self, photoset):
    for img in self.selected:
      self.dataManager.importPhoto(imageBase + img, photoset)
    self.selected = set()

    self.photo.refresh(self.dataManager.loader.PhotoStorage.findPhotos(imageBase),
        imageBase)

  def refresh(self):
    self.photo.refresh(self.dataManager.loader.PhotoStorage.findPhotos(imageBase),
        imageBase)

  def toggle(self, path):
    if (path in self.selected):
      self.selected -= set([path])
    else:
      self.selected.update(set([path]))

    if (len(self.selected) == 0):
      self.photosetAdd.canAdd = False
    else:
      self.photosetAdd.canAdd = True

    self.photosetAdd.showAdd()
