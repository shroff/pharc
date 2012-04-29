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
  """The PageManager is the GUI control object, managing all pages and associated GUI widgets.

    The PageManager itself initiates the Logic unit (DataManager) and passes this through to each
    GUI page or widget which needs it.  It also populates the initial patient list by running an
    empty query to the DataManager in order to pass to any necessary objects.

    Attributes:
        data: A pointer to the application's root datamanager object
        parent: The parent object which calls this instance
        currPatientList: the initial list of all patients currently stored
    """
  def __init__(self, parent):
    self.data = DataManager("patients")
    super(PageManager, self).__init__(parent)
    self.parent = parent
    
    q1 = DataManager.Query('first_name', 'sub', '')
    sresults = self.data.searchPatients([q1], None)
    self.currPatientList = [x for x in sresults.keys()]

    self.initUI()
    self.viewMain()

  def initUI(self):
    vbox = QVBoxLayout()

    self.mainpage = MainPage(self, "Doctor", self.data, self.currPatientList)
    self.editpage = PatientEditPage(self, self.data)
    self.importpage = ImportPage(self, self.data, self.currPatientList)

    vbox.addWidget(self.mainpage)
    vbox.addWidget(self.editpage)
    vbox.addWidget(self.importpage)

    self.setLayout(vbox)

  def viewDetails(self, patient):
    self.editpage.setPatient(patient)
    self.mainpage.setVisible(False)
    self.importpage.setVisible(False)
    self.editpage.setVisible(True)

  def viewMain(self):
    self.editpage.setVisible(False)
    self.importpage.setVisible(False)
    self.mainpage.setVisible(True)

  def viewImport(self):
    self.editpage.setVisible(False)
    self.mainpage.setVisible(False)
    self.importpage.setVisible(True)

  def triggerUpdate(self):
    self.importpage.modelUpdated()
    self.mainpage.modelUpdated()
