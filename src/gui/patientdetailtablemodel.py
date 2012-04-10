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

rowcount = 2;

#TODO: Link Model to logic
class PatientDetailTableModel(QStandardItemModel):
  def __init__(self):
    super(PatientDetailTableModel, self).__init__(rowcount, 2)

    self.setHeaders()

    self.fakeData()


  def setHeaders(self):
    self.setHeaderData(0, Qt.Horizontal, 'Treatment', role=Qt.DisplayRole)
    self.setHeaderData(1, Qt.Horizontal, 'Diagnosis', role=Qt.DisplayRole)

  def fakeData(self):
    self.setItem(0, 0, QStandardItem('a'))
    self.setItem(0, 1, QStandardItem('a'))
    self.setItem(1, 0, QStandardItem('a'))
    self.setItem(1, 1, QStandardItem('a'))
