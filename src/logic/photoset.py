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

    datamanager = None
    date = None
    patient = None # Patient that this photoset belongs to
    physicians = None # list of Physicians that care about this photoset
    notes = None # notes about this photoset, string
    diagnoses = None # list of diagnosis tags attached to this photoset
    treatments = None # list of treatment tags attached to this photoset
    uid = None # this photoset's unique identification number, integer
    photos = None # list of photos in this photoset

    loader = None # PhotosetLoader for this photoset
    
    def __init__(self):
        pass


    def add_treatment_by_string(self, treatment):
        """Adds a treatment to this photoset and updates indexes.

        Adds the given treatment to this photoset's list of
        treatments. Also adds this photoset to the treatment's list of
        photosets with this diagnosis to make lookups faster.

        Args:
            treatment: tag that will be used to look up the
                appropriate tag and add it to the photoset or, if no
                matching tag exists, to create a new tag and add this
                photoset to it.

        Returns:
            True if a new treatment tag was created, False otherwise

        Raises:
        """

        if not isinstance(treatment, Tag):
            raise TypeError("Adding a tag requires a Tag")

        if treatment in self.datamanager.treatments:
            self.datamanager.treatments[treatment].add(self)
            return True
        else:
            self.datamanager.treatments = {treatment : set([self])}
            return False

                
