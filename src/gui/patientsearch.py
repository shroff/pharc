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
    self.dataManager = dm
    self.searchResults = pList

    self.initUI()

  def initUI(self):
    vbox = QVBoxLayout()

    
    self.search = QWidget(self)
    self.search.setLayout(self.createSearch())
    self.create = QWidget(self)
    self.create.setLayout(self.createCreate())

    vbox.addWidget(self.search)
    vbox.addWidget(self.create)

    self.create.setVisible(False)

    self.setLayout(vbox)

  def createCreate(self):
    vbox = QVBoxLayout()

    vbox.addWidget(QLabel('Create a new patient'))

    hboxForm = QHBoxLayout()
    vboxLabels = QVBoxLayout()
    vboxLabels.addWidget(QLabel('First Name:'))
    vboxLabels.addWidget(QLabel('Last Name:'))
    vboxInputs = QVBoxLayout()
    self.fnameInput = QLineEdit()
    self.lnameInput = QLineEdit()
    vboxInputs.addWidget(self.fnameInput)
    vboxInputs.addWidget(self.lnameInput)
    hboxForm.addLayout(vboxLabels)
    hboxForm.addLayout(vboxInputs)

    hboxButtons = QHBoxLayout()
    hboxButtons.addStretch(1)
    cancelButton = QPushButton('Cancel')
    createButton = QPushButton('Create Patient')
    hboxButtons.addWidget(cancelButton)
    hboxButtons.addWidget(createButton)


    vbox.addLayout(hboxForm)
    vbox.addLayout(hboxButtons)

    QObject.connect(cancelButton, SIGNAL('clicked()'), self.switchSearch)
    QObject.connect(createButton, SIGNAL('clicked()'), self.createPatient)

    return vbox

  def createSearch(self):
    vbox = QVBoxLayout()

    self.searchBar = SearchBar(self, self.dataManager, True)
    self.patientTable = PatientTable(self, self.dataManager,
        self.searchResults, True)

    hbox = QHBoxLayout()
    addToPatient = QPushButton("Add to Patient")
    createPatient = QPushButton("Create Patient")
    hbox.addStretch(1)
    hbox.addWidget(addToPatient)
    hbox.addWidget(createPatient)

    vbox.addWidget(self.searchBar)
    vbox.addWidget(self.patientTable)
    vbox.addLayout(hbox)

    QObject.connect(addToPatient, SIGNAL('clicked()'), self.addToPatient)
    QObject.connect(createPatient, SIGNAL('clicked()'), self.switchCreate)

    return vbox


  def select(self, patient):
    self.parent.select(patient)

  def updateSearch(self, pats):
    self.searchResults = pats
    self.patientTable.updateSearch(pats)

  def createPatient(self):
    self.dataManager.makePatient(str(self.fnameInput.text()), str(self.lnameInput.text()))
    self.parent.triggerUpdate()
    self.searchBar.setSearch(self.fnameInput.text() + " " + self.lnameInput.text())
    self.switchSearch()

  def modelUpdated(self):
    self.patientTable.modelUpdated()

  def addToPatient(self):
    pass

  def switchCreate(self):
    self.search.setVisible(False)
    self.create.setVisible(True)

  def switchSearch(self):
    self.search.setVisible(True)
    self.create.setVisible(False)

