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
from logic.photo import Photo

class ImportPhoto(QWidget):
  def __init__(self, parent, name, path, checkable, checked = False):
    super(ImportPhoto, self).__init__()
    self.parent = parent
    self.name = name
    self.path = path
    self.checkable = checkable

    self.initUI(checked)

  def initUI(self, checked):
    vbox = QVBoxLayout()

    self.picLabel = QLabel()
    self.picLabel.setFixedSize(QSize(150, 150))

    if isinstance(self.name, Photo):
      name = self.name.name
    else:
      name = self.name

    image = QImage(self.path + name)
    pixmap = QPixmap.fromImage(image)
    if(not pixmap.isNull()):
      pixmap = pixmap.scaledToHeight(150)
      self.picLabel.setPixmap(pixmap)
      self.picLabel.setFixedSize(pixmap.size())

    self.picLabel.setFrameStyle(QFrame.Panel | QFrame.Box)

    hbox = QHBoxLayout()

    if self.checkable:
      nameLabel = QCheckBox(name, self)
      if(checked):
        nameLabel.setChecked(checked)
      QObject.connect(nameLabel, SIGNAL('stateChanged(int)'), self.toggle)
    else:
      nameLabel = QLabel(name)
    hbox.setAlignment(Qt.AlignCenter)
    hbox.addWidget(nameLabel)

    vbox.addWidget(self.picLabel)
    vbox.addLayout(hbox)

    self.setLayout(vbox)

  def toggle(self, arg):
    self.parent.toggle(self.name)
