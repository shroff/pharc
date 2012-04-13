#!/usr/bin/env python2
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

from . import db
from . import fs
from . import patientloader

def testDB():
    d = db.DB()
    d.exit()
    return

def testFS():
    f = fs.FS("Database")
    pl = patientloader.PatientLoader(None, f)

    patients = f.load_all_patients()
    for i in patients:
        pl.load_notes(i)
        pl.load_physicians(i)
        pl.load_photosets(i)
        print(i.nameFirst + " " + i.nameLast + ": " + i.uid)
        print("\t" + i.notes)
        print("\t" + str(i.physicians))
        print("\t" + str(i.photosets))

    f.exit()
    return

def main():
    testDB()
    testFS()
    return

if __name__ == " __main__":
    main()
else:
    main()
