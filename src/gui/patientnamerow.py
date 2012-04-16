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

class PatientNameRow(QWidget):
  def __init__(self):
    super(PatientNameRow, self).__init__()

    self.initUI()
    self.changing = False

  def initUI(self):
    self.changeFirstName = ChangeNameField(self)
    self.changeLastName = ChangeNameField(self)
    self.changeLastName.setVisible(False)

    self.editButton = QPushButton('Edit')
    self.cancelButton = QPushButton('Cancel')
    self.cancelButton.setVisible(False)

    hbox = QHBoxLayout()
    hbox.addWidget(QLabel('Patient Name: ', self))
    hbox.addWidget(self.changeFirstName)
    hbox.addWidget(self.changeLastName)
    hbox.addWidget(self.editButton)
    hbox.addWidget(self.cancelButton)

    QObject.connect(self.editButton, SIGNAL('clicked()'), self.nameChange)
    QObject.connect(self.cancelButton, SIGNAL('clicked()'), self.cancel)

    self.setLayout(hbox)

  def nameChange(self):
    if(self.changing):
      self.change()
    else:
      self.changeFirstName.setReadOnly(False)
      self.changeFirstName.setText(str(self.patient.nameFirst))
      self.changeFirstName.setFocus()

      self.changeLastName.setReadOnly(False)
      self.changeLastName.setVisible(True)
      self.changeLastName.setText(str(self.patient.nameLast))

      self.editButton.setText('Done')
      self.cancelButton.setVisible(True)
      self.changing = True

  def change(self):
    if (self.changeFirstName.text() != ''):
      print("Changing name to: " + self.changeFirstName.text() + " " +
          self.changeLastName.text())
    self.tempNameFirst = str(self.changeFirstName.text())
    self.tempNameLast = str(self.changeLastName.text())

    self.cancel()


  def cancel(self):
    self.changeFirstName.setReadOnly(True)
    self.changeLastName.setReadOnly(True)
    self.changeLastName.setVisible(False)

    self.editButton.setText('Edit')
    self.cancelButton.setVisible(False)

    self.changing = False
    self.changeFirstName.setText(str(self.tempNameFirst + " " + self.tempNameLast))

  def setPatient(self, p):
    self.patient = p
    self.changeFirstName.setText(str(self.patient.nameFirst + " " + self.patient.nameLast))
    self.tempNameFirst = self.patient.nameFirst
    self.tempNameLast = self.patient.nameLast

  def savePatient(self):
    self.patient.nameFirst = self.tempNameFirst
    self.patient.nameLast = self.tempNameLast


class ChangeNameField(QLineEdit):
  def __init__(self, sb):
    super(ChangeNameField, self).__init__(sb)

    self.setReadOnly(True)
    self.sb = sb

  def event(self, evt):
    if (evt.type() == QEvent.KeyPress) and ((evt.key() == Qt.Key_Enter) or
        (evt.key() == Qt.Key_Return)):
      self.sb.change()
      return True
    if (evt.type() == QEvent.KeyPress) and ((evt.key() == Qt.Key_Escape) or
        (evt.key() == Qt.Key_Return)):
      self.sb.cancel()
      return True

    return QLineEdit.event(self, evt)
