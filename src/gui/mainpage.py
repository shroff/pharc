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

from .searchbar import SearchBar
from .patientinfo import PatientInfo

import database.fs
from logic.datamanager import DataManager

#data = None

class MainPage(QWidget):
  def __init__(self, parent, name, dm):
    self.data = dm
    super(MainPage, self).__init__(parent)
    self.parent = parent
    self.initUI(name)

  def initUI(self, name):
    vbox = QVBoxLayout()
    vbox.addWidget(QLabel('Welcome ' + name, self))
    vbox.addWidget(SearchBar())
    vbox.addWidget(PatientInfo(self, self.data))

    self.setLayout(vbox)

  def viewDetails(self, index):
    self.parent.viewDetails(index)
