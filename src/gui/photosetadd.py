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

from .patientdetailtable import PatientDetailTable

class PhotosetAdd(QWidget):
  def __init__(self, parent, dm):
    super(PhotosetAdd, self).__init__(parent)
    self.parent = parent
    self.data = dm
    self.canAdd = False

    self.initUI()

  def initUI(self):
    vbox = QVBoxLayout()

    self.photosets = PatientDetailTable(self, self.data)

    hbox = QHBoxLayout()
    self.addToPhotoset = QPushButton("Add to Photoset")
    self.createPhotoset = QPushButton("Create Photoset")
    hbox.addStretch(1)
    hbox.addWidget(self.addToPhotoset)
    hbox.addWidget(self.createPhotoset)

    self.createPhotoset.setEnabled(False)
    self.addToPhotoset.setEnabled(False)

    vbox.addWidget(self.photosets)
    vbox.addLayout(hbox)
    self.setLayout(vbox)

    QObject.connect(self.addToPhotoset, SIGNAL('clicked()'), self.add)
    QObject.connect(self.createPhotoset, SIGNAL('clicked()'), self.create)


  def setPatient(self, patient):
    self.photosets.setPatient(patient)
    self.createPhotoset.setEnabled(True)
    self.patient = patient
    self.sel = -1
    self.showAdd()

  def add(self):
    pass

  def create(self):
    self.data.makePhotoset(self.patient)
    self.photosets.modelUpdated()

  def selected(self, row):
    self.sel = row
    self.showAdd()

  def showAdd(self):
    self.addToPhotoset.setEnabled(self.canAdd and (self.sel != -1))
