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

import db
import fs

# import sys
# sys.path.append('../logic')
from logic.patient import Photoset

class PhotosetLoader:

    def __init__(self, dbm, fsm):
        # there may be a better way of handling this, but it should do
        self.dbm = dbm
        self.fsm = fsm

    def load_photos(self, photoset):
        pass

    def load_diagnoses(self, patient):
        pass

    def load_treatments(self, patient):
        pass

    def load_diagnoses(self, photoset):
        pass

    def load_treatments(self, photoset):
        pass

    def load_tags(self, photoset):
        pass
