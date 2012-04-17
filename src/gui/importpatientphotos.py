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

from .importphoto import *

import random

imageBase = "images/"
imgs = ['caesar.jpg', 'puppy.jpg', 'kitty.jpg', 'punch.jpg']

class ImportPatientPhotos(QWidget):
  def __init__(self, parent):
    super(ImportPatientPhotos, self).__init__()
    self.parent = parent

    self.initUI()

  def initUI(self):
    vbox = QVBoxLayout()

    for x in range(1, 4):
      hbox = QHBoxLayout()
      hbox.setAlignment(Qt.AlignCenter)
      hbox.addWidget(ImportPhoto(self, imageBase + random.choice(imgs)))
      vbox.addLayout(hbox)


    sizeLabel = QLabel("")
    sizeLabel.setFixedSize(QSize(300, 1))
    vbox.addWidget(sizeLabel)

    self.setLayout(vbox)
