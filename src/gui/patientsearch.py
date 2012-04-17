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

from .searchbar import SearchBar
from .patienttable import PatientTable

class PatientSearch(QWidget):
  def __init__(self, parent, dm, pList):
    super(PatientSearch, self).__init__(parent)
    self.parent = parent
    self.data = dm
    self.searchResults = pList

    self.initUI()

  def initUI(self):
    vbox = QVBoxLayout()

    self.searchBar = SearchBar(self, self.data, True)
    self.patientTable = PatientTable(self, self.data, self.searchResults, True)

    hbox = QHBoxLayout()
    addToPatient = QPushButton("Add to Patient")
    createPatient = QPushButton("Create Patient")
    hbox.addStretch(1)
    hbox.addWidget(addToPatient)
    hbox.addWidget(createPatient)

    vbox.addWidget(self.searchBar)
    vbox.addWidget(self.patientTable)
    vbox.addLayout(hbox)
    self.setLayout(vbox)

    QObject.connect(addToPatient, SIGNAL('clicked()'), self.addToPatient)
    QObject.connect(createPatient, SIGNAL('clicked()'), self.createPatient)


  def select(self, patient):
    self.parent.select(patient)

  def updateSearch(self, pats):
    self.searchResults = pats
    self.patientTable.updateSearch(pats)

  def addToPatient(self):
    pass

  def createPatient(self):
    pass
