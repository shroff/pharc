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

from .patientsearchtablemodel import PatientSearchTableModel

import database.fs
from logic.datamanager import DataManager
from logic.patient import Patient

#data = None

class PatientSearchTable(QTableView):
  def __init__(self, parent, dm):
    self.data = dm
    super(PatientSearchTable, self).__init__(parent)
    self.parent = parent
    self.initUI()
    self.linkModel()

    self.connect(self, SIGNAL("clicked(QModelIndex)"), self.click)
    self.connect(self, SIGNAL("activated(QModelIndex)"), self.click)
    #self.connect(self, SIGNAL("doubleClicked(QModelIndex)"), self.detail)
    self.showMaximized()

  def initUI(self):
    self.setColumnWidth(0, 200)
    self.setColumnWidth(1, 200)


    self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.horizontalHeader().ResizeMode(QHeaderView.Stretch)
    self.horizontalHeader().setStretchLastSection(True)

  def linkModel(self):
    self.patientSearchTableModel = PatientSearchTableModel(self.data)
    self.setModel(self.patientSearchTableModel)
    self.updateGeometry()


  def click(self, index):
    pass

