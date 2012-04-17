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

#TODO: Link Model to logic
class PatientDetailTableModel(QStandardItemModel):
  def __init__(self, dm, patient):
    super(PatientDetailTableModel, self).__init__(0, 3)
    self.dataManager = dm
    self.patient = patient

    self.setHeaders()

    self.populate()

  def setHeaders(self):
    self.setHeaderData(0, Qt.Horizontal, 'Date', role=Qt.DisplayRole)
    self.setHeaderData(1, Qt.Horizontal, 'Treatments', role=Qt.DisplayRole)
    self.setHeaderData(2, Qt.Horizontal, 'Diagnoses', role=Qt.DisplayRole)

  def populate(self):
    self.rowcount = 0
    for ps in self.patient.photosets:
      self.setItem(self.rowcount, 0, QStandardItem(str(ps.date)))
      self.setItem(self.rowcount, 1, QStandardItem(", ".join(map(str,
        ps.treatments))))
      self.setItem(self.rowcount, 2, QStandardItem(", ".join(map(str,
        ps.diagnoses))))
      self.setData(self.index(self.rowcount, 0), ps, role=Qt.UserRole)
      self.setData(self.index(self.rowcount, 1), ps, role=Qt.UserRole)
      self.setData(self.index(self.rowcount, 2), ps, role=Qt.UserRole)
      self.rowcount=self.rowcount+1

