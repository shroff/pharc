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
    self.data = dm
    self.parent = parent
    self.initUI()

    self.connect(self, SIGNAL("clicked(QModelIndex)"), self.click)
    self.connect(self, SIGNAL("activated(QModelIndex)"), self.click)
    self.showMaximized()

  def initUI(self):
    self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.horizontalHeader().ResizeMode(QHeaderView.Stretch)
    self.horizontalHeader().setStretchLastSection(True)

  def linkModel(self):
    self.setModel(PatientDetailTableModel(self.data, self.patient))
    self.updateGeometry()


  def click(self, index):
    self.parent.selected(index.row())

  def setPatient(self, patient):
    self.patient = patient
    self.linkModel()
