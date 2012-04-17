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

class SearchBar(QWidget):
  def __init__(self, parent, dm, small = False):
    self.data = dm
    super(SearchBar, self).__init__()
    self.parent = parent
    self.small = small

    self.initUI()

  def initUI(self):
    self.search = QLineEdit(self)
    QObject.connect(self.search, SIGNAL('textEdited(QString)'), self.update)

    hbox = QHBoxLayout()
    if (not self.small):
      hbox.addWidget(QLabel('Search: ', self))
    hbox.addWidget(self.search)

    self.setLayout(hbox)

  def search(self, text):
    self.search.setText(text)
    self.update(text)

  def update(self, text):
    q1 = DataManager.Query('first_name', 'sub', str(text))
    q2 = DataManager.Query('last_name', 'sub', str(text))
#    q3 = DataManager.Query('diags', 'one', str(text))
#    q4 = DataManager.Query('treats', 'one', str(text))
    sresults = self.data.searchPatients([q1], None)
    sresults2 = self.data.searchPatients([q2], None)
    sresults.update(sresults2)
    echo = ""
    for (p,_) in sresults.items():
        echo += str(p) + "\n"
    print(echo[:-1])
    self.parent.updateSearch(sresults)

