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

class PatientNameRow(QWidget):
  def __init__(self):
    super(PatientNameRow, self).__init__()

    self.initUI()
    self.changing = False

  def initUI(self):
    self.changeNameField = ChangeNameField(self)
    self.editButton = QPushButton('Edit')
    self.cancelButton = QPushButton('Cancel')
    self.cancelButton.setVisible(False)

    hbox = QHBoxLayout()
    hbox.addWidget(QLabel('Patient Name: ', self))
    hbox.addWidget(self.changeNameField)
    hbox.addWidget(self.editButton)
    hbox.addWidget(self.cancelButton)

    QObject.connect(self.editButton, SIGNAL('clicked()'), self.nameChange)
    QObject.connect(self.cancelButton, SIGNAL('clicked()'), self.cancel)

    self.setLayout(hbox)

  def nameChange(self):
    if(self.changing):
      self.change()
    else:
      self.changeNameField.setReadOnly(False)
      self.changeNameField.setFocus()
      self.editButton.setText('Done')
      self.cancelButton.setVisible(True)
      self.changing = True

  def change(self):
    if (self.changeNameField.text() != ''):
      print "Changing name to: " + self.changeNameField.text()

    self.cancel()


  def cancel(self):
    self.changeNameField.setReadOnly(True)
    self.editButton.setText('Edit')
    self.cancelButton.setVisible(False)

    self.changing = False

  def setName(self, name):
    self.changeNameField.setText(str(name))



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
