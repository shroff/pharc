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


# I chose not to implement these as a pile of dictionaries because it
# made the search functions a bit cleaner.

import itertools
import logic.util

class TagList(object):

    """Holds a list of tags and provides methods for searching them.

    Attributes:
        tags: a list of tags.
    """

    tags = None # set of tags in the taglist

    def __init__(self):
        self.tags = set()

    def __contains__(self, item):
        """Membership operator. Returns True if the specified tag is
        in this taglist, otherwise False."""
        return item in self.tags

    def add(self, t):
        """Add Tag t to this TagList. Use this instead of the tags
        member for indexing purposes."""
        # no indices to update right now, but there might be some
        # later.
        self.tags.add(t)
        
    def match_fullstring_single(self, query):
        """Returns None or a tag whose name completely matches the
        query. If multiple tags match, results are undefined. There
        should only be one tag in the list with a given name."""
        results = [t for t in self.tags if t.match_fullstring(query)]
        if not results:         # no results
            return None
        return results[0]

    def match_substring_single(self, query):
        """Returns a list of tags whose names contain the query as a
        contiguous substring."""
        return [t for t in tags if t.match_substring(query)]

    def match_subsequence_single(self, query, n):
        # TODO: implement secondary sorting criterion.
        """Returns tag results sorted by the longest common
        subsequence between the tag name and the query.

        Returns a list of tags ranked by the length of the longest
        common subsequence between teh name of the tag and the query
        string. If n is None, returns a list of tags that each have
        the longest common subsequence length. If n is a number,
        returns that many results. Results are ordered first by the
        length of the longest common subsequence and second by the
        average of the index of the last character in the tag that was
        part of the lcs and the index of the first character in the
        tag that was part of the lcs (this prioritizes finding
        prefixes over spread-out or internal matches).
        
        Args:
            query: the string to check.
            n: the number of results to return or None for the tags
                with the longest common subsequence.

        Returns:
           A list of tags selected by the length of the longest common
           subsequence between the tag's name and the query.
        """
        results = [(t, t.match_common_subseq(query)) for t in tags]
        if n is None:
            maxl = -1;
            for t,tl in results:
                if tl > maxl:
                    maxl = tl
            return [t[0] for t in results if t[1] == maxl]
        else:
            results.sort(key=lambda a: a[1])
            return results[:n]

class Tag(object):

    value = None # string name of the tag
    photosets = None # set of photosets with this tag
    
    def __init__(self, name):
        self.value = name
        self.photosets = set()
    
    def match_substring(self, query):
        """Returns true if the tag's name contains the query as a
        contiguous substring."""
        return self.value.find(query) != -1

    def match_fullstring(self, query):
        """Returns true if the tag's name completely matches the
        query."""
        return query == self.value

    def match_common_subseq(self, query):
        """Returns the longest common subsequence for use in matching.

        Uses dynamic programming to compute the longest common
        subsequence between this tag's name and the query. Returns a
        tuple containing the longest common subsequence itself plus
        lists of indices indicating where the two strings coincided,
        in the form (result, [tag name indices], [query indices]). The
        indices are sorted largest to smallest because that was
        easier. For example:

        name:  1234
               ^^^^
        query: 1224533324
               ^^   ^   ^
        result: ("1234", [3,2,1,0], [9,5,1,0])

        name:  testing123testing
               ^ ^ ^     ^^^^
        query: thisisatest
               ^  ^^  ^^^^
        result: ('tsitest', [13,12,11,10,4,2,0], [10,9,8,7,4,3,0])

        Examples and code stolen from
        rosettacode.org/wiki/Longest_common_subsequence#Dynamic_Programming_6

        Args:
            query: the string to match against

        Returns:
            The computed LCS.

        Raises:
        """

        return logic.util.lcs(self.value, query)

    def __repr__(self):
        return str(self.value)
