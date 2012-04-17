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

class ImportPhoto(QWidget):
  def __init__(self, parent, name, path):
    super(ImportPhoto, self).__init__()
    self.parent = parent
    self.name = name
    self.path = path

    self.initUI()

  def initUI(self):
    vbox = QVBoxLayout()

    self.picLabel = QLabel()
    self.picLabel.setFixedSize(QSize(150, 150))

    image = QImage(self.path + self.name)
    pixmap = QPixmap.fromImage(image)
    if(not pixmap.isNull()):
      pixmap = pixmap.scaledToHeight(150)
      self.picLabel.setPixmap(pixmap)
      self.picLabel.setFixedSize(pixmap.size())

    self.picLabel.setFrameStyle(QFrame.Panel | QFrame.Box)

    hbox = QHBoxLayout()
    self.checkbox = QCheckBox(self.name, self)
    QObject.connect(self.checkbox, SIGNAL('stateChanged(int)'), self.toggle)
    hbox.setAlignment(Qt.AlignCenter)
    hbox.addWidget(self.checkbox)

    vbox.addWidget(self.picLabel)
    vbox.addLayout(hbox)

    self.setLayout(vbox)

  def toggle(self, arg):
    self.parent.toggle(self.name)
