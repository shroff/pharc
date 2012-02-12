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
