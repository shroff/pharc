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
        """
            Load the diagnoses for a given photoset.

            Arguments:
                photoset: The photoset who's diagnoses we want.

            Returns:
                The list of diagnoses.

            Throws:
                ?

        """
        return self.fsm.loadPhotosetDiagnoses(photoset)

    def loadTreatments(self, photoset):
        """
            Load the treatments for a given photoset.
            
            Arguments:
                photoset: The photoset who's treatments we want.

             Returns:
                The list of treatments.

             Throws:
                ?
        """
        return self.fsm.loadPhotosetTreatments(photoset)

    def loadTags(self, photoset):
        """
            Load the tags for a given photoset, that is both the diagnoses 
            and the treatments.

            Arguments:
                photoset: The photoset who's tags we want.

            Returns:
                The list of diagnoses and treatments.

            Throws:
                ?
        """
        list = loadDiagnoses(photoset)
        list.append(loadTreatments(photoset))
        return list

    def movePhotoset(self, photoset, toPatient):
        """
            Moves a photoset from one patient to another.

            Arguments:
                photoset:  The photoset we want to move.
                toPatient: The patient we want to move it to.

            Returns:
                N/A -- Sets photoset.patient to toPatient

            Throws:
                ?
        """
        if photoset.patient is None:
            self.fsm.createPhotoset(photoset, toPatient)
        else:
            fromDirectory = self.fsm.generatePhotosetDir(photoset)
            toDirectory = self.fsm.generatePhotosetDir(photoset, photoset.toPatient)
            self.fsm.copyPatient(photoset, fromDirectory, toDirectory)
            self.fsm.deletePhotoset(photoset)

        photoset.patient = toPatient

    def editTreatments(self, photoset, treatments):
        """
            Change the treatments of a photoset.

            Arguments:
                photoset:   The photoset who's treatments we want to change.
                treatments: What we want to set the treatments to.

            Returns:
                N/A

            Throws:
                ?
        """
        self.fsm.editPhotosetTreatments(photoset, treatments)

    def editDiagnoses(self, photoset, diagnoses):
        """
            Change the diagnoses of a photoset.

            Arguments:
                photoset:  The photoset who's treatments we want to change.
                diagnoses: What we want to set the diagnoses to.

            Returns:
                N/A

            Throws:
                ?
        """
        self.fsm.editPhotosetDiagnoses(photoset, diagnoses)

    def editDate(self, photoset, date):
        """
            Change the date of a photoset in the database.

            Arguments:
                photoset: The photoset who's date we want to change, 
                          photoset.date should be the old date.
                date:     A datetime object representing the new date for this photoset.

            Returns:
                N/A

            Throws:
                ?
        """
        fromDirectory = self.fsm.generatePhotosetDir(photoset, photoset.patient)
        uid = str(photoset.uid)
        toDirectory = self.fsm.generatePatientDir(photoset.patient) + "/" + \
            str(date.day).zfill(2) + "-" + str(date.month).zfill(2) + \
            "-" + str(date.year) + "#" + uid
        self.fsm.copyPhotoset(photoset, fromDirectory, toDirectory)
        self.fsm.dletePhotoset(photoset)

