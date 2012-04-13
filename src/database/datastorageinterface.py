# PHARC: a photo archiving application for physicians
# Copyright (C) 2012  Saul Reynolds-Haertle, James Cline
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

from .fs import FS
from .db import DB
from .patientstorage import PatientStorage
from .photosetstorage import PhotosetStorage
from .photostorage import PhotoStorage

# norvig.com/python-iaq.html
def abstract():
    """ This is a trick to enable abstract methods.

    Any method definition defined as:
      def method(self): abstract()
    that is not then defined in a class that inherits from this, when that method
    is called by something else, this will cause a runtime error.

    The exception returned also shows information about where the unimplemented
    method is.
    """
    import inspect
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')

class DataStorageInterface:
    """The interface for data loader classes.
       
         Both DB and FS will inherit from this class.
         It defines the methods that those classes must have for other classes to
         use.
    """

    # Initialize and do appropriate operations on startup
    def __init__(self, dbpath, fspath):

        self.FS = FS(fspath)
        self.DB = DB(dbpath)

        self.PatientStorage = PatientStorage(self.DB, self.FS)
        self.PhotosetStorage = PhotosetStorage(self.DB, self.FS)
        self.PhotoStorage = PhotoStorage(self.DB, self.FS)

    # Cleanup/validation before program termination
    def exit(self): abstract()

    # Returns if the data storage existed prior to class init
    def is_new(self): abstract()

    # Returns a list of all the patients
    def load_all_patients(self): abstract()
