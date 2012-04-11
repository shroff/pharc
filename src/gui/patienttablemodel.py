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
from logic.patient import Patient


class PatientTableModel(QStandardItemModel):
  def __init__(self, dm):
    super(PatientTableModel, self).__init__(0, 3)
    self.data = dm

    self.setHeaders()

    self.populate()


  def setHeaders(self):
    self.setHeaderData(0, Qt.Horizontal, 'Name', role=Qt.DisplayRole)
    self.setHeaderData(1, Qt.Horizontal, 'Treatment', role=Qt.DisplayRole)
    self.setHeaderData(2, Qt.Horizontal, 'Diagnosis', role=Qt.DisplayRole)

  def populate(self):
    self.rowcount = 0
    for p in self.data.patients:
      self.setItem(self.rowcount, 0, QStandardItem(p.name_first + " " + p.name_last))
      #self.setItem(num, 1, QStandardItem(p.treatments))
      #self.setItem(num, 2, QStandardItem(p.diagnoses))
      self.rowcount = self.rowcount+1
