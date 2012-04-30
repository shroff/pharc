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

from .patienttablemodel import *

import database.fs
from logic.datamanager import DataManager
from logic.patient import Patient

#data = None

class PatientTable(QTableView):
  def __init__(self, parent, dm, resultMap, small = False):
    super(PatientTable, self).__init__(parent)
    self.dataManager = dm
    self.parent = parent
    self.resultMap = resultMap
    self.small = small

    self.initUI()
    self.linkModel()


  def initUI(self):
    self.header = QHeaderView(Qt.Horizontal, self)
    self.header.ResizeMode(QHeaderView.ResizeToContents)
    self.header.setStretchLastSection(True)
    self.header.setSortIndicator(-1, Qt.AscendingOrder)
    self.header.setClickable(True)
    self.setHorizontalHeader(self.header)
    self.verticalHeader().setVisible(False)

    self.connect(self, SIGNAL("clicked(QModelIndex)"), self.view)
    if(not self.small):
      self.connect(self, SIGNAL("doubleClicked(QModelIndex)"), self.parent.viewDetails)
      self.connect(self, SIGNAL("activated(QModelIndex)"), self.parent.viewDetails)

    self.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.setAlternatingRowColors(True)
    self.setSelectionMode(self.SingleSelection)

    self.setSortingEnabled(True)

  def linkModel(self):
    self.patientTableModel = PatientTableModel(self.dataManager,
        self.resultMap, self.small)
    self.setModel(self.patientTableModel)
    self.updateGeometry()

    self.connect(self.selectionModel(), SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"), self.view)
    if(self.small):
      self.setColumnWidth(0, 200)
    else:
      self.verticalHeader().setDefaultSectionSize(100);
      self.setColumnWidth(0, 300)


  def view(self, index):
    self.parent.select(self.patientTableModel.getPatient(index))


  def updateSearch(self, pats):
    self.patientTableModel.updateSearch(pats)
    if(self.small):
      self.hideColumn(2)

  def modelUpdated(self):
    self.patientTableModel.modelUpdated()
