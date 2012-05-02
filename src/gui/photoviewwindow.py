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


import os
import sys
import subprocess

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class PhotoViewWindow(QMainWindow):
  def __init__(self, photos, title, dataManager):
    super(PhotoViewWindow, self).__init__()
    self.initUI(title, list(photos), dataManager)

    self.show()


  def initUI(self, title, photos, dataManager):
    self.resize(800, 600)
    self.setWindowTitle(title)

    self.setCentralWidget(PhotoViewWidget(self, photos, dataManager))


class PhotoViewWidget(QWidget):
  def __init__(self, parent, photos, dataManager):
    super(PhotoViewWidget, self).__init__()
    self.parent = parent
    self.photos = photos
    self.dataManager = dataManager
    self.initUI()

    self.index = 0
    self.cycle(0)

  def initUI(self):
    hbox = QHBoxLayout()
    self.image = QLabel()
    self.info = DetailsPanel(self)
    hbox.addWidget(self.image)
    hbox.addWidget(self.info)

    self.setLayout(hbox)


  def cycle(self, num):
    self.index = (self.index + num + len(self.photos))%len(self.photos)
    photo = self.photos[self.index]
    self.info.setPhoto(photo)
    path = self.dataManager.loader.PhotosetStorage.getPath(photo.photoset) + '/' + photo.name
    image = QImage(path)
    if(image.width() > self.width() or image.height() > self.height()):
      if(image.width()/self.width() > image.height()/self.height()):
        image = image.scaledToWidth(self.width())
      else:
        image = image.scaledToHeight(self.height())
    self.image.setPixmap(QPixmap.fromImage(image))



class DetailsPanel(QWidget):
  def __init__(self, parent):
    super(DetailsPanel, self).__init__()
    self.parent = parent
    self.initUI()
    self.setFixedSize(200, 500)
    self.cur = None

  def initUI(self):
    vbox = QVBoxLayout()
    self.name = QLabel()
    self.date = QLabel()
    self.photoname = QLabel()
    self.diagnosis = QLabel()
    self.treatment = QLabel()
    vbox.addWidget(self.name)
    vbox.addWidget(self.date)
    vbox.addWidget(self.photoname)
    vbox.addWidget(self.diagnosis)
    vbox.addWidget(self.treatment)

    self.editButton = QPushButton('Open in External Viewer')
    vbox.addWidget(self.editButton)

    buttonHBox = QHBoxLayout()
    prevButton = QPushButton('<')
    nextButton = QPushButton('>')
    buttonHBox.addWidget(prevButton)
    buttonHBox.addWidget(nextButton)
    vbox.addLayout(buttonHBox)

    self.doneButton = QPushButton('Done')
    vbox.addWidget(self.doneButton)

    QObject.connect(self.doneButton, SIGNAL('clicked()'), self.parent.parent.close)
    QObject.connect(nextButton, SIGNAL('clicked()'), self.nextImage)
    QObject.connect(prevButton, SIGNAL('clicked()'), self.prevImage)
    QObject.connect(self.editButton, SIGNAL('clicked()'), self.externalEditImage)

    self.setLayout(vbox)

  def setPhoto(self, photo):
    self.cur = photo
    photoset = photo.photoset
    self.name.setText('Patient Name:\n' + photoset.patient.nameFirst + " " +
        photoset.patient.nameLast)
    self.date.setText('Date:\n' + str(photoset.date))
    self.photoname.setText('Photo Name:\n' + str(photo.name))
    self.treatment.setText('Treatments:\n' + ",\n".join(map(str, photoset.patient.treatments)))
    self.diagnosis.setText('Diagnoses:\n' + ",\n".join(map(str, photoset.patient.diagnoses)))

  def nextImage(self):
    self.parent.cycle(1)

  def prevImage(self):
    self.parent.cycle(-1)

  def externalEditImage(self):
    path = self.cur.getData()
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', path))
    elif os.name == 'nt':
        os.startfile(path)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', path))
    
