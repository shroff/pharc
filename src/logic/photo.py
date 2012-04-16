# PHARC: a photo archiving application for physicians
# Copyright (C) 2012  Saul Reynolds-Haertle
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

class Photo(object):
    """A Photo stores and manages information about one photo.

    A singel Photo object stores the information required to work with
    a photo and provides functions that hide FS and GUI functionality
    from each other. It stores the filename of a photo (for example,
    "DSC0000001.jpg") as well as a pointer to the photoset that this
    photo is a part of so that the entire path can be
    constructed.

    Attributes:
        dm: a pointer to this photo's root datamanager object
        name: the filename of this photo. compose with photoset name
            to get the full path.
        photoset: the photoset that this photo belongs in
    """


    def __init__(self, name, psinit=None):
        self._photoset = psinit
        self._name = name

    def getData(self):
        return self.dm.loader.PhotoStorage.getPhotoData(self)

    def getname(self):
        return self._name
        pass
    def setname(self, value):
        self.dm.loader.PhotoStorage.renamePhoto(self, value)
        self._name = value
        pass
    def delname(self):
        pass
    name = property(getname, setname, delname, "")

    def getphotoset(self):
        return self._name
        pass
    def setphotoset(self, value):
        # move self on filesystem
        # self.dm.loader.PhotoStorage.movePhoto(self, value)
        
        # update old parent photoset
        
        # update new parent photoset
        
        # update _photoset
        # self._photoset = value
        pass
    def delphotoset(self):
        pass
    photoset = property(getphotoset, setphotoset, delphotoset, "")
