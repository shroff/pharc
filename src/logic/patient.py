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
    
    datamanager = None
    name_first = None # first name, string
    name_last = None # last name, string
    physicians = None # list of physicians that this patient interacts with
    photosets = None # list of photosets of this patient
    storage_diagnosis = None # diagnosis used for persistent storage location
    notes = None # notes about this patient, string
    uid = None # this patient's unique identification number, integer
    
    loader = None # PatientLoader for this patient

    @classmethod
    def __init__():
        pass


