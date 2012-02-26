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

