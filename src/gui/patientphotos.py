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
from database.photostorage import *

import random

class PatientPhotos(QScrollArea):
  def __init__(self, parent, data, checkable=True, horiz=False):
    super(PatientPhotos, self).__init__()
    self.parent = parent
    self.dataManager = data
    self.checkable=checkable
    self.horiz=horiz
    self.selected = set()
    self.refresh([], '')

  def refresh(self, images, imageDir):
    self.initUI(images, imageDir)

  def initUI(self, images, imageDir):
    imageDir = imageDir + '/'
    self.setWidget(self.createWidget(images, imageDir))
    if(self.horiz):
      self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
    else:
      self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)

    self.setBackgroundRole(QPalette.Light)

  def createWidget(self, images, imageDir):
    if(self.horiz):
      box = QHBoxLayout()
      self.setFixedHeight(230)
    else:
      box = QVBoxLayout()
      self.setFixedWidth(300)

    for x in images:
      pbox = QHBoxLayout()
      pbox.setAlignment(Qt.AlignCenter)
      pbox.addWidget(ImportPhoto(self, x, imageDir, self.checkable, x in self.selected))
      box.addLayout(pbox)

    photos = QWidget()
    photos.setLayout(box)
    
    return photos

  def setSelected(self, selected):
    self.selected = selected;


  def toggle(self, photo):
    self.parent.toggle(photo)

