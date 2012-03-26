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

class SearchBar(QWidget):
  def __init__(self):
    super(SearchBar, self).__init__()

    self.initUI()

  def initUI(self):
    self.searchField = SearchField(self)

    hbox = QHBoxLayout()
    hbox.addWidget(QLabel('Search: ', self))
    hbox.addWidget(self.searchField)

    self.setLayout(hbox)

  def search(self):
    if (self.searchField.text() == ''):
      return

#TODO: Implement searching
    print "Searching for " + self.searchField.text()


class SearchField(QLineEdit):
  def __init__(self, sb):
    super(SearchField, self).__init__(sb)

    self.sb = sb

  def event(self, evt):
    if (evt.type() == QEvent.KeyPress) and ((evt.key() == Qt.Key_Enter) or
        (evt.key() == Qt.Key_Return)):
      self.sb.search()
      return True

    return QLineEdit.event(self, evt)
