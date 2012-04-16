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

class Patient(object):
    """A Patient stores one patient's photosets and information.

    A single Patient object stores information about one patient as
    well as pointers to that patient's photosets. It manages lazy
    loading of photosets and thumbnails when the GUI asks for info to
    display. Note that hte patient does not contain any treatment or
    diagnosis tags! These are contained entirely in teh photosets, and
    a patient's treatment and diagnosis information is dyanmically
    constructed from their photosets.

    Attributes:
        datamanager: A pointer to this patient's root datamanager object
        nameFirst: The patient's first name as a string
        nameLast: The patient's last name as a string
        physicians: A set of physicians that this patient interacts with
        photosets: A set of photosets of this patient
        storage_diagnosis: The diagnosis this patient is stored under in the fs
        notes: notes about this patient as a big string
        uid: This patient's unique identification number. integer
    """
    dm = None

    def __init__(self, fname=None, lname=None, num=None):
        # the first three are loaded eagerly on database startup and
        # we don't need to trigger any lazy loading for them, so they
        # don't need to be properties
        self._nameFirst = fname
        self._nameLast = lname
        self.uid = num
        # these are all properties because they require some lazy
        # loading.
        self._physicians = None
        self._photosets = None
        self._storage_diagnosis = None
        self._notes = None

    def __repr__(self):
        return \
            "patient({0} {1}#{2}: {3} sets)".format(self.nameFirst,
                                                    self.nameLast,
                                                    str(self.uid),
                                                    str(len(self.photosets)))

    def getMostRecentPhotoset(self):
        return max(self.photosets, key=lambda x: x.date)

    def getphysicians(self):
        #print "physicians -> " + str(self._physicians)
        return self._physicians
    def setphysicians(self, value):
        #print "physicians <- " + str(value)
        self._physicians = value
    def delphysicians(slef):
        del self._physicians
    physicians = property(getphysicians, setphysicians, delphysicians, "")

    def name(self):
        return self.nameFirst + self.nameLast

    def getnameFirst(self):
        return self._nameFirst
    def setnameFirst(self, value):
        print("{0} --> nameFirst".format(str(value)))
        if (value != self._nameFirst):
            self.dm.loader.PatientStorage.editName(self, value, self._nameLast)
            self._nameFirst = value
    def delnameFirst(self):
        pass
    nameFirst = property(getnameFirst, setnameFirst, delnameFirst, "")
    def getnameLast(self):
        return self._nameLast
    def setnameLast(self, value):
        print("{0} --> nameLast".format(str(value)))
        if (value != self._nameLast):
            self.dm.loader.PatientStorage.editName(self, self._nameFirst, value)
            self._nameLast = value
    def delnameLast(self):
        pass
    nameLast = property(getnameLast, setnameLast, delnameLast, "")

    def getphotosets(self):
        if self._photosets is None:
            self._photosets = set()
            self.dm.loader.PatientStorage.loadPhotosets(self)
        #print "photosets -> " + str(self._photosets)
        return self._photosets
    def setphotosets(self, value):
        #print "photosets <- " + str(value)
        self._photosets = value
    def delphotosets(slef):
        del self._photosets
    photosets = property(getphotosets, setphotosets, delphotosets, "")


    def getnotes(self):
        if self._notes is None:
            self._notes = self.dm.loader.PatientStorage.loadNotes(self)
        #print "notes -> " + str(self._notes)
        return self._notes
    def setnotes(self, value):
        #print "notes <- " + str(value)
        self._notes = value
    def delnotes(slef):
        del self._notes
    notes = property(getnotes, setnotes, delnotes, "")


    def getdiagnoses(self):
        result = set()
        for ps in self.photosets:
            result |= ps.diagnoses
        return result
    def setdiagnoses(self, value):
        raise NotImplementedError("I haven't figured out a good way to handle changing patient diagnoses.")
    def deldiagnoses(slef):
        raise NotImplementedError("I haven't figured out a good way to handle deleting patient diagnoses.")
    diagnoses = property(getdiagnoses, setdiagnoses, deldiagnoses, "")


    def gettreatments(self):
        result = set()
        for ps in self.photosets:
            result |= ps.treatments
        return result
    def settreatments(self, value):
        raise NotImplementedError("I haven't figured out a good way to handle changing patient treatments.")
    def deltreatments(slef):
        raise NotImplementedError("I haven't figured out a good way to handle deleting patient treatments.")
    treatments = property(gettreatments, settreatments, deltreatments, "")
