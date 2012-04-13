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

class PhotosetStorage:

    def __init__(self, dbm, fsm):
        # there may be a better way of handling this, but it should do
        self.dbm = dbm
        self.fsm = fsm

    def loadPhotos(self, photoset):
        pass

    def loadDiagnoses(self, photoset):
        return self.fsm.loadPhotosetDiagnoses(photoset)

    def loadTreatments(self, photoset):
        return self.fsm.loadPhotosetTreatments(photoset)

    def loadTags(self, photoset):
        list = loadDiagnoses(photoset)
        list.append(loadTreatments(photoset))
        return list

    def movePhotoset(self, photoset, toPatient):
        self.fsm.createPhotoset(photoset, toPatient)

        if photoset.patient is None:
            pass
        else:
            self.fsm.deletePhotoset(photoset)

        photoset.patient = toPatient

    def editTreatments(self, photoset, treatments):
        self.fsm.ediPhotosetTreatments(photoset, treatments)

    def editDiagnoses(self, photoset, diagnoses):
        self.fsm.ediPhotosetDiagnoses(photoset, diagnoses)
