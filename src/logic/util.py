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


# basic utility functions for pharc



def lcs(a, b):
    """Returns the longest common subsequence for use in matching.

    Uses dynamic programming to compute the longest common subsequence
    between the sequences a and b. Returns a tuple containing the
    longest common subsequence itself plus lists of indices indicating
    where the two strings coincided, in the form (result, [a indices],
    [b indices]). The indices are sorted largest to smallest because
    that was easier. For example:

    a:      1234
            ^^^^
    b:      1224533324
            ^^   ^   ^
    result: ("1234", [3,2,1,0], [9,5,1,0])

    a:      testing123testing
            ^ ^ ^     ^^^^
    b:      thisisatest
            ^  ^^  ^^^^
    result: ('tsitest', [13,12,11,10,4,2,0], [10,9,8,7,4,3,0])

    Note that this function works on any sequence of comparable
    elements, not just strings!

    Examples and code stolen from
    rosettacode.org/wiki/Longest_common_subsequence#Dynamic_Programming_6

    Args:
        a, b: sequences to match against each other

    Returns:
        The computed LCS.

    Raises:
    """

    result = ""
    a_index = []
    b_index = []

    lengths = \
        [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = \
                    max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            result = a[x-1] + result
            a_index.append(x-1)
            b_index.append(y-1)
            x -= 1
            y -= 1
    return (result, a_index, b_index)

