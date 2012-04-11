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

rowcount = 2;
#data = None

#TODO: Link Model to logic
class PatientTableModel(QStandardItemModel):
  def __init__(self, dm):
    super(PatientTableModel, self).__init__(rowcount, 3)
    self.data = dm
#    self.data = DataManager("C:/Users/Michael/Desktop/DB/Database")

    self.setHeaders()

    #self.fakeData()
    self.realData()


  def setHeaders(self):
    self.setHeaderData(0, Qt.Horizontal, 'Name', role=Qt.DisplayRole)
    self.setHeaderData(1, Qt.Horizontal, 'Treatment', role=Qt.DisplayRole)
    self.setHeaderData(2, Qt.Horizontal, 'Diagnosis', role=Qt.DisplayRole)

  def fakeData(self):
    self.setItem(0, 0, QStandardItem('a'))
    self.setItem(0, 1, QStandardItem('a'))
    self.setItem(0, 2, QStandardItem('a'))
    self.setItem(1, 0, QStandardItem('a'))
    self.setItem(1, 1, QStandardItem('a'))
    self.setItem(1, 2, QStandardItem('a'))
    for p in range(2,50):
      for i in range(0,3):
        self.setItem(p, i, QStandardItem('a'))

  def realData(self):
    num = 0
    for p in self.data.patients:
      self.setItem(num, 0, QStandardItem(p.name_first + " " + p.name_last))
      #self.setItem(num, 1, QStandardItem(p.treatments))
      #self.setItem(num, 2, QStandardItem(p.diagnoses))
      num=num+1

#  def getDataManager()
