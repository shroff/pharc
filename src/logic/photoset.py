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

import logic.tags as tags

class Photoset(object):

    dm = None # reference to the datamanger at teh top of the hierarchy
    date = None
    patient = None # Patient that this photoset belongs to
    physicians = None # list of Physicians that care about this photoset
    notes = None # notes about this photoset, string
    diagnoses = None # set of diagnosis tags attached to this photoset
    treatments = None # set of treatment tags attached to this photoset
    uid = None # this photoset's unique identification number, integer
    photos = None # list of photos in this photoset

    def __init__(self):
        self._treatments = None
        self._diagnoses = None

    def __repr__(self):
        return \
            "photoset({0}#{1}, t:{2}, d:{3})".format( \
            str(self.date),
            str(self.uid),
            self.treatments,
            self.diagnoses)

    def addDiagnosis(self, diagnosis):
        """Refers to tag list and adds appropriate tag.

        Adds the diagnosis to this photoset's list of diagnosiss. If
        diagnosis is a string, looks up the list of existing
        diagnosiss, finds one that matches the diagnosis name exactly
        or creates one if no suitable tags exist, and adds this
        photoset to this tag and updates indices. If a tag, just adds
        it and updates indices.

        Args:
            diagnosis: the name of the tag to add to this photoset

        Returns:
            The tag that was added to this photoset (useful if
            creating by string)
        """
        
        t = None
        if isinstance(diagnosis, str):
            t = self.dm.diagnoses.match_fullstring_single(diagnosis)
            if not t: # no matching tag, so make a new one
                t = self.dm.diagnoses.create(diagnosis)
        else:
            t = diagnosis

        # update indices
        if self not in t.photosets:
            t.photosets.add(self)
        if t not in self._diagnoses:
            self._diagnoses.add(t)

        # update fs
        self.dm.loader.PhotosetStorage.editDiagnoses(self)
            
        return t

    def addTreatment(self, treatment):
        """Refers to tag list and adds appropriate tag.

        Adds the treatment to this photoset's list of treatments. If
        treatment is a string, looks up the list of existing
        treatments, finds one that matches the treatment name exactly
        or creates one if no suitable tags exist, and adds this
        photoset to this tag and updates indices. If a tag, just adds
        it and updates indices.

        Args:
            treatment: the name of the tag to add to this photoset

        Returns:
            The tag that was added to this photoset (useful if
            creating by string)
        """
        
        t = None
        if isinstance(treatment, str):
            t = self.dm.treatments.match_fullstring_single(treatment)
            if not t: # no matching tag, so make a new one
                t = self.dm.treatments.create(treatment)
        else:
            t = treatment

        # update indices
        if self not in t.photosets:
            t.photosets.add(self)
        if t not in self._treatments:
            self._treatments.add(t)

        # update fs
        self.dm.loader.PhotosetStorage.editTreatments(self)
            
        return t


    def gettreatments(self):
        if self._treatments is None:
            self._treatments = set()
            tstrings = self.dm.loader.PhotosetStorage.loadTreatments(self)
            for s in tstrings:
                self.addTreatment(s)
        # print "treatments -> " + str(self._treatments)
        return self._treatments
    def settreatments(self, value):
        #print "treatments <- " + str(value)
        self._treatments = value
        self.dm.loader.editTreatments(self)
    def deltreatments(slef):
        del self._treatments
    treatments = property(gettreatments, settreatments, deltreatments, "")

    def getdiagnoses(self):
        if self._diagnoses is None:
            self._diagnoses = set()
            dstrings = self.dm.loader.PhotosetStorage.loadDiagnoses(self)
            for s in dstrings:
                self.addDiagnosis(s)
        # print "diagnoses -> " + str(self._diagnoses)
        return self._diagnoses
    def setdiagnoses(self, value):
        #print "diagnoses <- " + str(value)
        self._diagnoses = value
        self.dm.loader.PhotosetStorage.editDiagnoses(self)
    def deldiagnoses(slef):
        del self._diagnoses
    diagnoses = property(getdiagnoses, setdiagnoses, deldiagnoses, "")

