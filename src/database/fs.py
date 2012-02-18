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

from dataloaderinterface import DataLoaderInterface
import os, sys

sys.path.append('../logic')
#from ..logic import patient
from patient import Patient

class FS(DataLoaderInterface):
	"""A filesystem manager"""

	# Initialize and do appropriate operations on startup
	def __init__(self, root):
		# Where the FS storage is located
		self.root = root;

		exists = os.path.isdir(root)

		if not exists:
			print "FS: root directory does not exist, creating " + self.root
			self.new_FS = True

			# create the root directory
			os.mkdir(root)
			# there is nothing more to do until the user adds data
		else:
			self.new_FS = False

		return

	# Cleanup/validation before program termination
	def exit(self):
		return

	# Returns if the data storage existed prior to class init
	def is_new(self):
		return self.new_FS

	# Returns a list of all the patients
	def load_all_patients(self):
		# There is nothing to load
		if self.is_new():
			return None

		patients = []

		items = os.listdir(self.root)
		# TODO: Probably not right
		for i in items:
			if os.path.isdir(self.root + "/" + i):
				p = Patient()
				# Parse filename
				name = i.split('#')[0]
				name = name.split()
				p.name_first = name[1]
				p.name_last = name[0][:-1]
				p.uid = i.split('#')[1]
				# Add new patient to the list
				patients.append(p)

		return patients

	def load_patient_notes(self, patient):
		if self.is_new():
			# TODO: error codes
			return None

		directory = self.root + "/" + patient.name_last + ", " + patient.name_first + "#" + patient.uid
		if os.path.isdir(directory):
			try:
				f = open(directory + "/notes.txt")
				notes = f.read()
				f.close()
			except IOError as (errno, strerror):
				print "IOError [{0}]: {1}".format(errno, sterror)
				# TODO: error codes
				return None
				
			return notes
		else:
			# TODO: error codes
			return None

