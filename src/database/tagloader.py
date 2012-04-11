# PHARC: a photo archiving application for physicians
# Copyright (C) 2012  Saul Reynolds-Haertle, James Cline
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

import db
import fs

# import sys
# sys.path.append('../logic')
from logic.patient import Patient
from logic.photoset import Photoset
from logic.tags import Tag
from logic.tags import TagList

class TagLoader:

	def __init__(self, dbm, fsm):
		this.dbm = dbm
		this.fsm = fsm

	def load_patient_tags(self, patient):

		for photoset in patient.photosets:
			load_photoset_tags( photoset )

	def load_photoset_tags(self, photoset):

		self.fsm.load_photoset_tags( photoset )
