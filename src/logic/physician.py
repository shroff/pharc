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


class Physician(object):
    
    datamanager = None

    loader = None # PhysicianLoader for this Physician
    
    def __init__(self):
        self.name_first = None # first name, string
        self.name_last = None # last name, string
        self.uid = None # uid, integer
        self.patients = None # list of patients that this physician interacts with

