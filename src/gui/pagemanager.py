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

from .mainpage import *
from .patienteditpage import *
from .importpage import *

import database.fs
from logic.datamanager import DataManager

#data = None

class PageManager(QWidget):
  def __init__(self, parent):
    self.data = DataManager("../database")
    super(PageManager, self).__init__(parent)
    self.parent = parent

    self.initUI()
    self.viewMain()

  def initUI(self):
    vbox = QVBoxLayout()

    self.mainpage = MainPage(self, "Doctor", self.data)
    self.editpage = PatientEditPage(self, self.data)
    self.importpage = ImportPage(self, self.data)

    vbox.addWidget(self.mainpage)
    vbox.addWidget(self.editpage)
    vbox.addWidget(self.importpage)

    self.setLayout(vbox)

  def viewDetails(self, index):
    self.editpage.setPatient(self.data.patients[index])
    self.editpage.setVisible(True)
    self.mainpage.setVisible(False)
    self.importpage.setVisible(False)

  def viewMain(self):
    self.editpage.setVisible(False)
    self.mainpage.setVisible(True)
    self.importpage.setVisible(False)

  def viewImport(self):
    self.editpage.setVisible(False)
    self.mainpage.setVisible(False)
    self.importpage.setVisible(True)
