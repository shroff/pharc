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

class FS(DataLoaderInterface):
	"""A filesystem manager"""

	# Initialize and do appropriate operations on startup
	def __init__(self, root):
		# Where the FS storage is located
		self.root = root;

		exists = os.path.isdir(root)

		if not exists:
			self.new_FS = True

			os.mkdir(root)

		return

	# Cleanup/validation before program termination
	def exit(self):
		return

	# Returns if the data storage existed prior to class init
	def isNew(self):
		return self.new_FS
