# -*- coding: utf-8 -*-

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

# TODO too much duped code for looking up entities by uid

import os
import sys
import database.datastorageinterface as dsi
from logic.datamanager import DataManager
import readline
import cmd
import datetime
import dateutil.parser

class CommandLineInterface(cmd.Cmd):
    """Implements a dead simple command-line interface for interactive
    testing."""

    prompt = "\033[94m[PHARC]$\033[0m "

    def getEntitiesByUID(self, target, rtype="patient"):
        """Gets a list of entities using the UID "target".

        Will always return a list, even if only one entity is found.

        rtpye is a string denoting what type of entity to return. The
        semantics are determined by exactly what is given and what is
        requested. Generally, returns everything even remotedly
        related. For example, requesting physicians and giving a
        patient UID will return all of that patient's
        physicians. Physician-photoset relations are a bit weird as a
        result. rtype can be any of "patient", "physician", or
        "photoset".
        
        this function will return patients by default.
        """
        
        ents = None
        if target < 65536:      # target is patient
            # figure out which patient the user is talking about
            q = DataManager.Query("id", "", int(target))
            sresults = self.dm.searchPatients([q], None)
            pats = [x[0] for x in sresults]
            if rtype == "patient":
                return pats
            elif rtype == "physician":
                # TODO get physician entities
                pass
            elif rtype == "photoset":
                result = []
                for p in pats:
                    result |= p.photosets
                return result
        elif target < 70000:    # target is physician
            # TODO get entity by physician
            if rtype == "patient":
                pass
            elif rtype == "physician":
                pass
            elif rtype == "photoset":
                pass
        else:                   # target is photoset
            q = DataManager.Query("id", "", int(args))
            sresults = self.dm.searchPhotosets([q], None)
            psets = [x for x in sresults if x.uid == target]
            if rtype == "patient":
                return [x.patient for x in psets]
            elif rtype == "physician":
                # TODO get physician entities
                pass
            elif rtype == "photoset":
                return psets

    def load_database(self, target):
        self.dm = DataManager(target)
        return

    def do_listPatients(self, args):
        echo = ""
        for p in self.dm.patients:
            echo += str(p) + "\n"
        print(echo[:-1])

    def do_findPatients(self, args):
        args = args.strip().split()
        q = DataManager.Query(args[0], args[1], args[2])
        sresults = self.dm.searchPatients([q], None)
        pats = [x[0] for x in sresults]
        
        echo = ""
        for p in pats:
            echo += str(p) + "\n"
        print(echo[:-1])

    def do_listPhotosets(self, args):
        pats = None
        if args == "":          # list all photosets
            pats = self.dm.patients
        elif int(args) <= 70000: # list all photosets from a patient
            pats = self.getEntitiesByUID(int(args), rtype="patient")
        else:                   # list a particualr photoset
            ps = [x for x in self.dm.searchPhotosets(None, None) if x.uid == int(args)]
            print(str(ps[0].patient) + ": " + str(ps[0]))
            return

        if len(pats) == 0:
            print("No patients found")
            return

        echo = ""
        for p in pats:
            echo += str(p) + "\n"
            psl = list(p.photosets)
            for i in range(0, len(psl) - 1):
                echo += "  ├─" + str(psl[i]) + "\n"
            if len(psl) > 0:
                echo += "  └─" + str(psl[-1]) + "\n"
        print(echo[:-1])
        
    def do_editPhotoset(self, args):
        args = args.split(" ")
        ps = [x for x in self.dm.searchPhotosets(None, None) if x.uid == int(args[0])]
        if not ps:
            return
        ps = ps[0]
        if args[1] == "date":
            d = dateutil.parser.parse(args[2])
            ps.date = d
        if args[1] == "+treat":
            str(ps.addTreatment(args[2]))
        if args[1] == "-treat":
            pass
        if args[1] == "+diag":
            str(ps.addDiagnosis(args[2]))
        if args[1] == "-diag":
            pass
    def do_editPatient(self, args):
        if args[1] == "fname":
            pass
        if args[1] == "lname":
            pass
        if args[1] == "notes":
            pass
        if args[1] == "+phys":
            pass
        if args[1] == "-phys":
            pass

    def do_loadRecentPhotoset(self, args):
        pats = None
        if args == "":
            pats = self.dm.patients
        else:
            # figure out which patient the user is talking about
            q = DataManager.Query("id", "", int(args))
            sresults = self.dm.searchPatients([q], None)
            pats = [x[0] for x in sresults]
        
        if len(pats) == 0:
            print("No patients found")
            return

        echo = ""
        for p in pats:
            echo += p.nameFirst + " " + p.nameLast + ": " + str(p.getMostRecentPhotoset()) + "\n"
        print(echo[:-1])

    def do_findPhotosets(self, args):
        pass

    def do_EOF(self, args):
        return True
    
    def do_lp(self, args):
        self.do_listPatients(args)
    def do_fp(self, args):
        self.do_findPatients(args)
    def do_lps(self,args):
        self.do_listPhotosets(args)
    def do_lt(self,args):
        self.do_loadTags(args)
    def do_fps(self, args):
        self.do_findPhotosets(args)
    def do_eps(self, args):
        self.do_editPhotoset(args)
    def do_ep(self, args):
        self.do_editPatient(args)

    
