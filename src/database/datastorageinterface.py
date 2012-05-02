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

import database.fs
import database.patientstorage as patientstor
import database.photosetstorage as photosetstor
import database.photostorage as photostor

class DataStorageInterface:
    """The interface for data loader classes.
    """

    # Initialize and do appropriate operations on startup
    def __init__(self, fspath):

        self.FS = database.fs.FS(fspath)

        self.PatientStorage = patientstor.PatientStorage(self.FS)
        self.PhotosetStorage = photosetstor.PhotosetStorage(self.FS)
        self.PhotoStorage = photostor.PhotoStorage(self.FS)

