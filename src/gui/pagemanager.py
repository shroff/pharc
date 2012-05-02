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
from .photoviewwindow import *

import export.sendtoppt
import export.sendtoemail

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

    self.selected = set()

    self.emailthread = export.sendtoemail.ExportThread()
    self.connect(self.emailthread, SIGNAL("finished()"), self.exportEmailDone)
    self.connect(self.emailthread, SIGNAL("terminated()"), self.exportEmailDone)
    self.connect(self.emailthread, SIGNAL("emailExportDone(int)"), self.exportEmailResult)

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
    self.importpage.refresh()

  def triggerUpdate(self):
    self.importpage.modelUpdated()
    self.mainpage.modelUpdated()

  def toggle(self, path):
    if (path in self.selected):
      self.selected -= set([path])
    else:
      self.selected.update(set([path]))

  def clearSelection(self):
    self.selected = set()
    self.editpage.clearSelection()

  def viewSelection(self):
    if(len(self.selected) > 0):
      PhotoViewWindow(self.selected, 'Selected Photos', self.data)


  def exportSelectionToPresentation(self):
    (filename, ok) = QInputDialog.getText(self.parent, "Enter Filename", "Presentation name:", text="presentation.odp")
    if ok:
      export.sendtoppt.export_presentation(self.selected, filename, True)
    else:
      self.parent.statusBar().showMessage("Canceled", 60000)




  def exportSelectionToEmail(self):
    # non-threaded version
    # export.sendtoemail.export_email(self.selected, "sreynoldshaertle@gmail.com")

    # threaded version
    
    (email, ok) = QInputDialog.getText(self.parent, "Enter Destination", "Email Address:")
    if ok:
      self.emailthread.export(self.selected, email)
      self.parent.statusBar().showMessage("sending email...", 60000)
    else:
      self.parent.statusBar().showMessage("Canceled", 60000)
  def exportEmailDone(self):
    print("export email done")
    pass
  def exportEmailResult(self, status):
    print("export email result: %d" % status)
    self.parent.statusBar().clearMessage()
    if status == -1:            # could not get MX addr
      self.parent.statusBar().showMessage("Could not find mail server - bad address; internet connected?", 10000)
    if status == -2:
      self.parent.statusBar().showMessage("Could not connect to mail server - Timed out", 10000)
    if status == 0:
      self.parent.statusBar().showMessage("Successfully sent email.", 10000)

