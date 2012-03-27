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
from mainpage import *

class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()

    self.initUI()
    self.createMenus()

    self.show()

  def initUI(self):
    self.resize(800, 600)
    self.setWindowTitle("Photo Archiving System")

    self.setCentralWidget(MainPage("Abhishek"))


  def createMenus(self):
    #exitAction = QAction(QIcon('exit.png') 'E&xit', self)
    exitAction = QAction('E&xit', self)
    exitAction.setShortcut('Ctrl+Q')
    exitAction.setStatusTip('Exit Application')
    exitAction.triggered.connect(qApp.quit)

    self.statusBar()

    menuBar = self.menuBar()
    fileMenu = menuBar.addMenu('&File')
    fileMenu.addAction(exitAction)

