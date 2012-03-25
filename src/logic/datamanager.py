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
import collections

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
        
    Query = collections.namedtuple('Query', ['field', 'match', 'arg'])
    def searchPatients(self, queries, n):
        ##########################################################
        ##
        ##  FIXME: is there a better way to do this than to pass
        ##  around all these damn strings? There has to be
        ##  something. Python doesn't do enums very well...
        ##
        ##########################################################
        """Does searches.

        A general function for advanced searches. Returns a list of
        objects that fit the given parameters.

        Args:

            queries: a list of "Query" namedtuples containing
                parameters for the search. Each element of the list is
                a tuple of the form (field, match, arg). The result
                will satisfy to _all_ parameters and will contain the
                indicated ranking information. The field and match
                fields of a search param are strings and the last is
                determined by teh first two. The same parameter can be
                specified multiple times and it will apply multiple
                times; all results will still satisfy all passed
                params. If a ranking query is submitted multiple
                times, results are undefined, but the returned scores
                will attempt to reflect a 'do what I mean'
                interpretation.
                
                field       match type    semantics
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

                field  arg: type(arg)
                       "match" constraint or ranking: semantics
                int    arg: An int
                       ""      c:  exact match with UID.
                string arg: A string
                       exact   c:  _exact_ string match with arg.
                       pre     c:  arg is a prefix of first_name
                       post    c:  arg is a suffix of first_name
                       sub     c:  arg is an exact substring
                       lcs     r:  rank results by longest common subsequence with arg
                strlst arg: a string which is then split by commas
                       ex_one  c:  at least one of the toks must be in the physician list
                       ex_all  c:  all tokens must be exactly in the physician list
                       lcs_one r:  rank by best single longest-common-subsequence correspondence
                       lcs_all r:  rank by maximum correspondence on lcs (wiki://assignment_problem)
                tag    arg: a list of strings
                       one     cr: at least one tag in the query is present in the patient's list
                       all-q   c:  every tag in the query is present in the patient's list
                       all-p   cr: every tag in the patient's list is present in the query
                       exact   c:  the query and the patient's tag list match exactly
                notes  arg: a string
                       one     cr: at least one of the words in the query occur in the notes
                       all     c:  all of the words in the query occur in the notes
                       exact   cr: the exact string is in the notes
                       without c:  none of the words occur in the notes

            n: how many results to return at most. If this is set to
                None, it is entirely possible that every patient in
                the database will be returned.

        Returns:
            A list of (patient, scores) tuples. Returns an empty list
            of no patients were found that fit the constraints. Every
            patient in the list will satisfy _all_ of the parameters
            of the query. scores is a dictionary that maps strings to
            particular scores assigned by the search function. These
            are the scores that will be returned:
            
            key         value semantics
            "fname_lcs" the length of the lcs between the query and the patient's first_name
            "lname_lcs" the length of the lcs between the query and the patient's last_name
            "diags"     number of diagnosis tags in both the query and the patient's list
            "treats"    number of treatment tags in both the query and the patient's list
            "phys_one"  length of the single best lcs match in the patient's list of physicians
            "phys_all"  sum of the lcs lengths in the max-weight matching of query params to physicians
            "notes_one" number of times words in a query string occur in the notes
            "notes_ex"  number of times exact string queries occur in the notes
            
            scores for which a query does not exist to measure against
            will not be reported. For example, if no diagnosis tags
            are specified, "diags" cannot be calculated and will not
            be returned.

            If multiple queries are submitted that would produce the
            same score, results are undefined, but the implementation
            will attempt to return a reasonable "do-what-I-mean"
            interpretation.
            """        

        ##########################################################
        # first big chunk: define methods for constraining results

        # The first person to touch valid_patients is going to
        # constrain the list of patients hugely, potentially from the
        # entire list of patients to the empty set. For that reason,
        # the first constrain operation behaves completely
        # differently. We pull this off by starting valid_patients as
        # None and having the first person to touch it turn it into a
        # set() with patients in it.
        valid_patients = None

        # the valid_patients thing is a hack to get around python 2's
        # badwrong handling of scope in local functions.
        def constrainId((f, m, a), valid_patients=valid_patients):
            if valid_patients is None:
                valid_patients = set([p for p in self.patients if p.uid == a])
            else:
                valid_patients = set([p for p in valid_patients if p.uid == a])
            return valid_patients
        def constrainFirstName((f, m, a), valid_patients=valid_patients):
            return valid_patients
        def constrainLastName((f, m, a), valid_patients=valid_patients):
            return valid_patients
        def constrainDiagnoses((f, m, a), valid_patients=valid_patients):
            return valid_patients
        def constrainTreatments((f, m, a), valid_patients=valid_patients):
            return valid_patients
        def constrainPhysicians((f, m, a), valid_patients=valid_patients):
            return valid_patients
        def constrainNotes((f, m, a), valid_patients=valid_patients):
            return valid_patients

        ##########################################################
        # second big chunk: define methods for ranking results

        result = list()
        def rankId((f, m, a), valid_patients=valid_patients):
            pass
        def rankFirstName((f, m, a), valid_patients=valid_patients):
            pass
        def rankLastName((f, m, a), valid_patients=valid_patients):
            pass
        def rankDiagnoses((f, m, a), valid_patients=valid_patients):
            pass
        def rankTreatments((f, m, a), valid_patients=valid_patients):
            pass
        def rankPhysicians((f, m, a), valid_patients=valid_patients):
            pass
        def rankNotes((f, m, a), valid_patients=valid_patients):
            pass

        ##########################################################
        # third big chunk: map constraints over patient list

        constraint_parse = {("id", ""):constrainId,
                            ("first_name", "exact"):constrainFirstName,
                            ("first_name", "pre"):constrainFirstName,
                            ("first_name", "post"):constrainFirstName,
                            ("first_name", "sub"):constrainFirstName,
                            ("last_name", "exact"):constrainLastName,
                            ("last_name", "pre"):constrainLastName,
                            ("last_name", "post"):constrainLastName,
                            ("last_name", "sub"):constrainLastName,
                            ("diags", "one"):constrainDiagnoses,
                            ("diags", "all-q"):constrainDiagnoses,
                            ("diags", "all-p"):constrainDiagnoses,
                            ("diags", "exact"):constrainDiagnoses,
                            ("treats", "one"):constrainTreatments,
                            ("treats", "all-q"):constrainTreatments,
                            ("treats", "all-p"):constrainTreatments,
                            ("treats", "exact"):constrainTreatments,
                            ("phys", "ex_one"):constrainPhysicians,
                            ("phys", "ex_all"):constrainPhysicians,
                            ("notes", "one"):constrainNotes,
                            ("notes", "all"):constrainNotes,
                            ("notes", "exact"):constrainNotes,
                            ("notes", "without"):constrainNotes,
                            }
        constraints = [q for q in queries if (q.field, q.match) in constraint_parse.keys()]

        ##########################################################
        # fourth big chunk: map rankings over patient list

        rankings_parse = {("first_name", "lcs"):rankFirstName,
                          ("last_name", "lcs"):rankLastName,
                          ("diags", "one"):rankDiagnoses,
                          ("diags", "all-p"):rankDiagnoses,
                          ("treats", "one"):rankDiagnoses,
                          ("treats", "all-p"):rankTreatments,
                          ("phys", "lcs_one"):rankPhysicians,
                          ("phys", "lcs_all"):rankPhysicians,
                          ("notes", "one"):rankNotes,
                          ("notes", "exact"):rankNotes,
                          }
        rankings = [q for q in queries if (q.field, q.match) in rankings_parse.keys()]

        ##########################################################
        # fifth big chunk: constrain, rank, and return

        # apply all the constraints; valid_patients 
        for q in constraints:
            valid_patients = constraint_parse[(q.field, q.match)](q)

        # if we've got nothing, return nothing
        if valid_patients is None:
            return []

        # set up the results: list of (patient, scoredict) tuples.
        for p in valid_patients:
            result.append((p, {"fname_lcs":None,
                               "lname_lcs":None,
                               "diags":None,
                               "treats":None,
                               "phys_one":None,
                               "phys_all":None,
                               "notes_one":None,
                               "notes_ex":None,
                               }))

        # now we go through the rankings and populate the score
        # dictionaries.
        for q in rankings:
            constraint_parse[(q.field, q.match)](q)

        return result
