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

class DataManager(object):
    """The DataManager is the root object in the logic package.

    The DataManager manages all of the data. It contains lists of
    physicians and patients and starts the initial loading of data
    from storage. Each data manager essentially represents one
    hospital's worth of data.
    
    Attributes:
        patients: a list of all of the patients in the system
        physicians: a list of all of the physicians in the system
        loader: a link to the filesystem interface
        treatments: a dictionary mapping treatment names to a set of photosets
        diagnoses: a dictionary mapping diagnosis names to a set of photosets
    """

    patients = None # list of all patients in the system
    physicians = None # list of all the physicians in the system
    loader = None # DataManagerLoader for this DataManager
    treatments = None # taglist
    diagnoses = None # taglist
    
    def __init__(class filesystem_location):
        """Opens a datamanagerloader and begins populating the system.
        
        Initializes a DataManagerLoader and loads some initial data
        from persistent storage.

        Args:
            filesystem_location: A filesystem path to the root
                directory of the persistent storage.
        
        Returns:
            A pointer to a new DataManager.

        Raises:
            IOError: Could not initialize the DataManagerLoader
        """
        pass


