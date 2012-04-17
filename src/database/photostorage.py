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

class PhotoStorage:
    def __init__(self, dbm, fsm):
        # there may be a better way of handling this, but it should do
        self.dbm = dbm
        self.fsm = fsm

    def importPhoto(self, path, photoset):
        """
            Imports a photo from outside the database and places it into
            the database, specifically inside a given photoset.

            Arguments:
                path:     The path to the external photo.
                photoset: The photoset we wish to store it in.

            Returns:
                N/A

            Throws:
                ?
        """
        self.fsm.importPhoto(path, photoset)

    def getPhotoData(self, photo):
        """
            Loads the photo image data.

            Arguments:
                photo: The photo object who's data we want.

            Returns:
                The image data of the photo.

            Throws:
                ?
        """
        return self.fsm.loadPhoto(photo)

    def renamePhoto(self, photo, toName):
        """
            Renames a photo's file.

            Arguments:
                photo: The photo object we want to rename.
                name:  The new name for the photo.

            Return:
                N/A

            Throws:
                ?
        """
        self.fsm.renamePhoto(photo, toName)

    def movePhoto(self, photo, toPhotoset):
        """
            Moves a photo from one photoset to another.

            Arguments:
                photo:      The photo object we want to move.
                toPhotoset: The photoset we want to move the photo to.

            Returns:
                N/A

            Throws:
                ?
        """
        self.fsm.movePhoto(photo, toPhotoset)

    def findPhotos(self, path):
        return self.fsm.findPhotos(path)
