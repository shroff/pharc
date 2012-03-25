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

import tags
import database.fs

class DataManager(object):
    """The DataManager is the root object in the logic package.

    The DataManager manages all of the data. It contains lists of
    physicians and patients and starts the initial loading of data
    from storage. Each data manager essentially represents one
    hospital's worth of data. This also presents a set of functions
    for searching for things.
    
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
    
    def __init__(self, filesystem_location):
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

        self.loader = database.fs.FS(filesystem_location)

        self.treatments = tags.TagList()
        self.diagnoses = tags.TagList()
        self.patients = self.loader.load_all_patients()
        self.physicians = []


    def searchPatients(self, query, n):
        """Does searches.

        A general function for advanced searches. Returns a list of
        objects that fit the given parameters.

        Args:

            queries: a list of tuples containing parameters for the
                search. Each element of the list is a tuple of the
                form (field, match, arg). The result will satisfy to
                _all_ parameters and will contain the indicated
                ranking information. The field and match fields of a
                search param are strings and the last is determined by
                teh first two. The same parameter can be specified
                multiple times and it will apply multiple times. If a
                ranking query is submitted multiple times, results are
                undefined but rankings will attempt to reflect a 'do
                what I mean' interpretation.
                
                field       match type
                id          int
                first_name  string
                last_name   string
                diags       tag
                treats      tag
                phys        strlst
                notes       notes

                What gets passed in as the arg, legal values for the
                match, and how the match causes the arg to be
                interpreted.

                int    arg: An int
                       ""      exact match with UID.
                string arg: A string
                       exact   _exact_ string match with arg
                       pre     arg is a prefix of first_name
                       post    arg is a suffix of first_name
                       sub     arg is an exact substring
                       lcs     rank results by longest common subsequence with arg
                strlst arg: a string which is then split by commas
                       ex_one  at least one of the toks must be in the physician list
                       ex_all  all tokens must be exactly in the physician list
                       lcs_one rank by best single longest-common-subsequence correspondence
                       lcs_all rank by maximum correspondence on lcs (wiki://assignment_problem)
                tag    arg: a list of strings
                       one     at least one tag in the query is present in the patient's list
                       all-q   every tag in the query is present in the patient's list
                       all-p   every tag in the patient's list is present in the query
                       exact   the query and the patient's tag list match exactly
                notes  arg: a string
                       one     at least one of the words in the query occur in the notes
                       all     all of the words in the query occur in the notes
                       exact   the exact string is in the notes
                       without none of the words occur in the notes

            n: how many results to return at most. If this is set to
                None, it is entirely possible that every patient in
                the database will be returned.

        Returns:
            A list of (patient, scores) tuples. Every patient in the
            list will satisfy _all_ of the parameters of the
            query. scores is a dictionary that maps strings to
            particular scores assigned by the search function. These
            are the scores that will be returned:
            
            key         value semantics
            "id_dist"   the distance between the specified uid and the patient's UID
            "fname_lcs" the length of the lcs between the query and the patient's first_name
            "lname_lcs" the length of the lcs between the query and the patient's last_name
            "diags"     number of diagnosis tags in both the query and the patient's list
            "treats"    number of treatment tags in both the query and the patient's list
            "phys_one"  length of the single best lcs match in the patient's physicians
            "phys_all"  sum of the lcs lengths in the maximum weight matching for physicians
            "notes_one" number of words in the query string that occur in the notes
            "notes_ex"  number of strings which occur exactly in the notes
            """        
        pass
