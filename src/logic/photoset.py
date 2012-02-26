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

class Photoset(object):

    datamanager = None # reference to the datamanger at teh top of the hierarchy
    date = None
    patient = None # Patient that this photoset belongs to
    physicians = None # list of Physicians that care about this photoset
    notes = None # notes about this photoset, string
    diagnoses = None # set of diagnosis tags attached to this photoset
    treatments = None # set of treatment tags attached to this photoset
    uid = None # this photoset's unique identification number, integer
    photos = None # list of photos in this photoset

    loader = None # PhotosetLoader for this photoset
    
    def __init__(self, datamanager):
        self.datamanager = datamanager
        self.treatments = set()
        self.diagnoses = set()
    
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

        match = self.datamanager.treatments.match_fullstring(treatment)
        if not match: # no matching tag, so make a new one and add it
                      # to the list
            match = Tag(treatment)
            self.datamanager.treatments.add(match)
        match.photosets.add(self)
        self.treatments.add(match)
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
        
        if self in treatment.photosets and treatment in self.treatments:
            return True
        
        treatment.photosets.add(self)
        self.treatments.add(treatment)
        return False
