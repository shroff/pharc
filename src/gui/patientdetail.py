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

import random

imageBase = "images/"
imgs = ['caesar.jpg', 'puppy.jpg', 'kitty.jpg', 'punch.jpg']

class PatientDetail(QWidget):
  def __init__(self, parent):
    super(PatientDetail, self).__init__(parent)
    self.parent = parent

    self.initUI()

  def initUI(self):
    self.setFixedSize(QSize(200, 450))
    vbox = QVBoxLayout()

    self.picLabel = QLabel()
    self.picLabel.setFixedSize(QSize(150, 150))
    self.nameLabel = QLabel('Name: ')
    self.diagLabel = QLabel('Diagnosis: ')
    self.tmtLabel = QLabel('Treatment: ')
    self.detailsButton = QPushButton('View Details')

    vbox.addWidget(self.picLabel)
    vbox.addWidget(self.nameLabel)
    vbox.addWidget(self.diagLabel)
    vbox.addWidget(self.tmtLabel)
    vbox.addWidget(self.detailsButton)

    self.setLayout(vbox)

    QObject.connect(self.detailsButton, SIGNAL('clicked()'), self.viewDetails)

  def setRandom(self):
    self.setPicture(imageBase + random.choice(imgs))

  def setPicture(self, imgpath):
    print(imgpath)
    image = QImage(imgpath)
    pixmap = QPixmap.fromImage(image)
    if(not pixmap.isNull()):
      pixmap = pixmap.scaledToHeight(150)
      self.picLabel.setPixmap(pixmap)
      self.picLabel.setFixedSize(pixmap.size())

  def setName(self, name):
    self.nameLabel.setText('Name: ' + name)

  def setTreatment(self, tmt):
    self.tmtLabel.setText('Treatment: ' + tmt)

  def setDiagnosis(self, diag):
    self.diagLabel.setText('Diagnosis: ' + diag)

  def viewDetails(self):
    self.parent.viewDetails()
