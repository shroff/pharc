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

from patienttable import PatientTable
from patientdetail import PatientDetail

class PatientInfo(QWidget):
  def __init__(self, parent):
    super(PatientInfo, self).__init__(parent)
    self.parent = parent
    self.initUI()

  def initUI(self):
    hbox = QHBoxLayout()
    self.patientTable = PatientTable(self)
    self.patientDetail = PatientDetail(self)
    self.patientDetail.setVisible(False)
    hbox.addWidget(self.patientTable)
    hbox.addWidget(self.patientDetail)

    self.setLayout(hbox)


  def viewInfo(self, row, col):
    self.patientDetail.setVisible(True)
    print row
    print col

  def viewDetails(self):
    if(self.patientDetail.isVisible()):
      self.parent.viewDetails()
