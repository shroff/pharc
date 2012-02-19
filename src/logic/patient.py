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
        name_first: The patient's first name as a string
        name_last: The patient's last name as a string
        physicians: A set of physicians that this patient interacts with
        photosets: A set of photosets of this patient
        storage_diagnosis: The diagnosis this patient is stored under in the fs
        notes: notes about this patient as a big string
        uid: This patient's unique identification number. integer
    """

    loader = None

    def __init__(self):
        self.datamanager = None
        self.name_first = None
        self.name_last = None
        self.physicians = []
        self.photosets = []
        self.storage_diagnosis = None
        self.notes = None
        self.uid = None


