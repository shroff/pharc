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

    def match_substring(self, query):
        """Returns a list of tags whose names contain the query as a
        contiguous substring."""
        return [t for t in tags if t.match_substring(query)]

    def match_fullstring(self, query):
        """Returns None or a tag whose name completely matches the
        query. If multiple tags match, results are undefined. There
        should only be one tag in the list with a given name."""
        results = [t for t in tags if t.match_fullstring(query)]
        if not results:         # no results
            return None
        return results[0]

    def match_common_subseq(self, query, n):
        """Returns tag results sorted by the longest common
        subsequence between the tag name and the query.

        Returns a set of tags ranked by the length of the longest
        common subsequence between teh name of the tag and the query
        string. If n is None, returns an unordered list of tags that
        each have the longest common subsequence length. If n is a
        number, returns that many results, ordered by the length of
        the common subsequence between teh tag's name and the
        query.
        
        Args:
            query: the string to check.
            n: the number of results to return or None for the tags
                with the longest common subsequence.

        Returns:
           A list of tags selected by the length of the longest common
           subsequence between the tag's name and the query.
        """
        pass

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

        result = ""
        name_index = []
        query_index = []
        
        lengths = \
            [[0 for j in range(len(query)+1)] for i in range(len(self.value)+1)]
        # row 0 and column 0 are initialized to 0 already
        for i, x in enumerate(self.value):
            for j, y in enumerate(query):
                if x == y:
                    lengths[i+1][j+1] = lengths[i][j] + 1
                else:
                    lengths[i+1][j+1] = \
                        max(lengths[i+1][j], lengths[i][j+1])
        # read the substring out from the matrix
        x, y = len(self.value), len(query)
        while x != 0 and y != 0:
            if lengths[x][y] == lengths[x-1][y]:
                x -= 1
            elif lengths[x][y] == lengths[x][y-1]:
                y -= 1
            else:
                assert self.value[x-1] == query[y-1]
                result = self.value[x-1] + result
                name_index.append(x-1)
                query_index.append(y-1)
                x -= 1
                y -= 1
        return (result, name_index, query_index)
