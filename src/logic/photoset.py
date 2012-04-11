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

from logic.datamanager import DataManager
from logic.tags import Tag

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

    def add_diagnosis_by_string(self, diagnosis):
        """Refers to tag list and adds appropriate tag.

        Adds the named diagnosis to this photoset's list of
        diagnosiss. Looks up the list of existing diagnosiss, finds
        one that matches the diagnosis name exactly or creates one,
        and adds this photoset to this tag and updates indices.

        Args:
            diagnosis: the name of the tag to add to this photoset

        Returns:
            The tag that was added to this photoset.
        """

        match = self.dm.diagnoses.match_fullstring_single(diagnosis)
        if not match: # no matching tag, so make a new one and add it
                      # to the list
            match = Tag(diagnosis)
            self.dm.diagnoses.add(match)
        match.photosets.add(self)
        self._diagnoses.add(match)
        return match
    
    
    def add_diagnosis_by_tag(self, diagnosis):
        """Adds this tag to the photoset.

        Adds the given diagnosis to this photoset's list of
        diagnosiss. Also adds this photoset to the diagnosis's list of
        photosets. Note that this method assumes that the given tag is
        the correct tag!
        
        Args:
            diagnosis: tag to add to this photoset.

        Returns:
            True if this photoset already had the tag and the tag
                already had the photoset, False otherwise.

        Raises:
        """
        
        if self in diagnosis.photosets and diagnosis in self._diagnoses:
            return True
        
        diagnosis.photosets.add(self)
        self._diagnoses.add(diagnosis)
        return False

    def add_treatment_by_string(self, treatment):
        """Refers to tag list and adds appropriate tag.

        Adds the named treatment to this photoset's list of
        treatments. Looks up the list of existing treatments, finds
        one that matches the treatment name exactly or creates one,
        and adds this photoset to this tag and updates indices.

        Args:
            treatment: the name of the tag to add to this photoset

        Returns:
            The tag that was added to this photoset.
        """

        match = self.dm.treatments.match_fullstring_single(treatment)
        if not match: # no matching tag, so make a new one and add it
                      # to the list
            match = Tag(treatment)
            self.dm.treatments.add(match)
        match.photosets.add(self)
        self._treatments.add(match)
        return match
    
    
    def add_treatment_by_tag(self, treatment):
        """Adds this tag to the photoset.

        Adds the given treatment to this photoset's list of
        treatments. Also adds this photoset to the treatment's list of
        photosets. Note that this method assumes that the given tag is
        the correct tag!
        
        Args:
            treatment: tag to add to this photoset.

        Returns:
            True if this photoset already had the tag and the tag
                already had the photoset, False otherwise.

        Raises:
        """
        
        if self in treatment.photosets and treatment in self._treatments:
            return True
        
        treatment.photosets.add(self)
        self._treatments.add(treatment)
        return False


    def gettreatments(self):
        if self._treatments is None:
            self._treatments = set()
            tstrings = self.dm.loader.load_photoset_treatments(self)
            for s in tstrings:
                self.add_treatment_by_string(s)
        # print "treatments -> " + str(self._treatments)
        return self._treatments
    def settreatments(self, value):
        #print "treatments <- " + str(value)
        self._treatments = value
    def deltreatments(slef):
        del self._treatments
    treatments = property(gettreatments, settreatments, deltreatments, "")

    def getdiagnoses(self):
        if self._diagnoses is None:
            self._diagnoses = set()
            dstrings = self.dm.loader.load_photoset_diagnoses(self)
            for s in dstrings:
                self.add_diagnosis_by_string(s)
        # print "diagnoses -> " + str(self._diagnoses)
        return self._diagnoses
    def setdiagnoses(self, value):
        #print "diagnoses <- " + str(value)
        self._diagnoses = value
    def deldiagnoses(slef):
        del self._diagnoses
    diagnoses = property(getdiagnoses, setdiagnoses, deldiagnoses, "")

