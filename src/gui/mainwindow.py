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
from .pagemanager import *

class MainWindow(QMainWindow):
  """The MainWindow is just that: the initial window of the application's GUI.

    The MainWindow itself initiates the menus, and various widgets and parents.

    Attributes:
        pageManager: A pointer to the GUI's control object
    """
  def __init__(self):
    super(MainWindow, self).__init__()

    self.initUI()
    self.createMenus()

    self.show()

  def initUI(self):
    self.resize(800, 600)
    self.setWindowTitle("Photo Archiving System")

    self.pageManager = PageManager(self)
    self.setCentralWidget(self.pageManager)


  def createMenus(self):
    menuBar = self.menuBar()

    fileMenu = menuBar.addMenu('&File')

    importAction = QAction('Check for I&mports', self)
    importAction.setShortcut('Ctrl+I')
    importAction.setStatusTip('Check for photos to import')
    importAction.triggered.connect(self.pageManager.viewImport)
    fileMenu.addAction(importAction)

    #exitAction = QAction(QIcon('exit.png') 'E&xit', self)
    exitAction = QAction('E&xit', self)
    exitAction.setShortcut('Ctrl+Q')
    exitAction.setStatusTip('Exit Application')
    exitAction.triggered.connect(qApp.quit)
    fileMenu.addAction(exitAction)


    selectionMenu = menuBar.addMenu('&Selection')

    clearSelectionAction = QAction('C&lear Selection', self)
    clearSelectionAction.setStatusTip('Clear Selected Photos')
    clearSelectionAction.triggered.connect(self.pageManager.clearSelection)
    selectionMenu.addAction(clearSelectionAction)

    viewSelectionAction = QAction('V&iew Selection', self)
    viewSelectionAction.setShortcut('Ctrl+w')
    viewSelectionAction.setStatusTip('View Selected Photos')
    viewSelectionAction.triggered.connect(self.pageManager.viewSelection)
    selectionMenu.addAction(viewSelectionAction)

    self.statusBar()

