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

import os
import sys
import database.fs
import logic.datamanager
import readline
import cmd

class CommandLineInterface(cmd.Cmd):
    """Implements a dead simple command-line interface for interactive
    testing."""

    def load_database(self, target):
        self.dm = logic.datamanager.DataManager("test/Database")
        return

    def do_listPatients(self, args):
        echo = ""
        for p in self.dm.patients:
            echo += str(p) + "\n"
        print echo

    def do_findPatients(self, args):
        pass

    def do_listPhotosets(self, args):
        # figure out which patient the user is talking about
        # p = None
        # for pat in self.dm.patients:
            
        
        echo = ""
        for p in self.dm.patients:
            echo += str(p) + "\n"
            for i in xrange(0, len(p.photosets) - 2):
                echo += " ├" + str(p.photosets[i]) + "\n"
            if len(p.photosets) > 0:
                echo += " └" + str(p.photosets[-1])
        print echo

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
    def do_fps(self, args):
        self.do_findPhotosets(args)

    
