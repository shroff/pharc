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

from .patientdetailtablemodel import PatientDetailTableModel

class PatientDetailTable(QTableView):
  def __init__(self, parent, dm):
    super(PatientDetailTable, self).__init__()
    self.dataManager = dm
    self.parent = parent
    self.initUI()

    self.connect(self, SIGNAL("clicked(QModelIndex)"), self.click)
    self.connect(self, SIGNAL("activated(QModelIndex)"), self.click)

  def initUI(self):
    self.horizontalHeader().ResizeMode(QHeaderView.ResizeToContents)
    self.horizontalHeader().setStretchLastSection(True)
    self.verticalHeader().setVisible(False)
    self.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.setAlternatingRowColors(True)
    self.setSelectionMode(self.SingleSelection)
    self.setMinimumSize(QSize(100, 100))

  def linkModel(self):
    self.setModel(PatientDetailTableModel(self.dataManager, self.patient))
    self.connect(self.selectionModel(), SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"), self.click)
    self.updateGeometry()

  def click(self, index):
    ps = self.model().data(index, role=Qt.UserRole)
    self.parent.selected(ps)

  def setPatient(self, patient):
    self.patient = patient
    self.linkModel()

  def modelUpdated(self):
    self.linkModel()
