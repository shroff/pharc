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

# import logic.datamanager as datamanager
# import logic.patient import patient


class PatientTableModel(QStandardItemModel):
  def __init__(self, dm, pList):
    super(PatientTableModel, self).__init__(0, 3)
    self.data = dm
    self.currPatientList = pList
    self.rowcount = 0

    self.setHeaders()
    self.populate()


  def setHeaders(self):
    self.setHeaderData(0, Qt.Horizontal, 'Name', role=Qt.DisplayRole)
    self.setHeaderData(1, Qt.Horizontal, 'Treatment', role=Qt.DisplayRole)
    self.setHeaderData(2, Qt.Horizontal, 'Diagnosis', role=Qt.DisplayRole)

  def populate(self):
    self.removeRows(0, self.rowcount)

    self.rowcount = 0
#    for p in self.data.patients:
    for p in self.currPatientList:
      c1 = QStandardItem(p.nameFirst + " " + p.nameLast)
      c1.setEditable(False)
      c2 = QStandardItem(", ".join(map(str, p.treatments)))
      c2.setEditable(False)
      c3 = QStandardItem(", ".join(map(str, p.diagnoses)))
      c3.setEditable(False)
      
      self.setItem(self.rowcount, 0, c1)
      self.setItem(self.rowcount, 1, c2)
      self.setItem(self.rowcount, 2, c3)
      self.rowcount = self.rowcount+1

  def updateSearch(self, pats):
    self.currPatientList = pats
    self.populate()

  def update(self):
    self.populate()
