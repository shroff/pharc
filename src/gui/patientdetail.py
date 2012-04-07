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


class PatientDetail(QWidget):
  def __init__(self):
    super(PatientDetail, self).__init__()
    self.initUI()

  def initUI(self):
    self.setMinimumSize(200, 300)
    self.setMaximumSize(200, 300)
    vbox = QVBoxLayout()
    self.nameLabel = QLabel('Name: ')
    self.diagLabel = QLabel('Diagnosis: ')
    self.tmtLabel = QLabel('Treatment: ')
    vbox.addWidget(self.nameLabel)
    vbox.addWidget(self.diagLabel)
    vbox.addWidget(self.tmtLabel)

    self.setLayout(vbox)

  def setName(self, name):
    self.nameLabel.setText('Name: ' + name)

  def setTreatment(self, tmt):
    self.tmtLabel.setText('Treatment: ' + tmt)

  def setDiagnosis(self, diag):
    self.diagLabel.setText('Name: ' + diag)
