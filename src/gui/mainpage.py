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

from .searchbar import SearchBar
from .patientinfo import PatientInfo

import database.fs
from logic.datamanager import DataManager

#data = None

class MainPage(QWidget):
  def __init__(self, parent, name, dm, pList):
    self.data = dm
    super(MainPage, self).__init__(parent)
    self.parent = parent
    self.currPatientList = pList
    self.initUI(name)
    

  def initUI(self, name):
    vbox = QVBoxLayout()
    vbox.addWidget(QLabel('Welcome ' + name, self))
    self.searchBar = SearchBar(self, self.data)
    vbox.addWidget(self.searchBar)
    self.patientInfo = PatientInfo(self, self.data, self.currPatientList)
    vbox.addWidget(self.patientInfo)

    self.setLayout(vbox)

  def viewDetails(self, patient):
    self.parent.viewDetails(patient)

  def updateSearch(self, pats):
    self.currPatientList = pats
    self.patientInfo.updateSearch(pats)

  def triggerUpdate(self):
    self.parent.triggerUpdate()

  def modelUpdated(self):
    self.patientInfo.modelUpdated()
