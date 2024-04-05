"""
Crossword and Wordsearch creator on the fly.
"""

import array
import itertools
import random


class RandomProduct:
    """Infinite generator of Cartesian product elements."""

    def __init__(self, iterables):
        self.lists = list(map(list, iterables))

    def __iter__(self):
        return self

    def __next__(self):
        return tuple(map(random.choice, self.lists))


class WordGrid(tuple):
    DEFAULT_CHAR = "*"
    directions = [
        (0, +1),  # Across
        (+1, 0),  # Down
        (0, -1),  # Backwards
        (-1, 0),  # Up
        (+1, +1),  # Across
        (+1, -1),  # Across
        (-1, +1),  # Across
        (-1, -1),  # Across
    ]
    product_generator = itertools.product
    notouch = False

    def __new__(cls, rows, cols, words=None):
        row_initializer = cls.DEFAULT_CHAR*cols
        return super().__new__(
            cls, [array.array('u', row_initializer) for i in range(rows)]
        )

    def __init__(self, rows, cols, words=None):
        self.rows = rows
        self.cols = cols
        if words is not None:
            self.addwords(*words, inplace=True)

    def __str__(self, lpad="| ", rpad=" |", space=" "):
        joiner = rpad + "\n" + lpad
        lines = map(space.join, self)
        info = f"{self.rows}x{self.cols}"
        return lpad + joiner.join(lines) + rpad + "\n" + info

    def output(self, inplace=True):
        if not inplace:
            print(self)

    def addwords(self, *words, directions=None, inplace=True):
        if directions is None:
            directions = self.directions
        self.addwords_recursive(
            sorted(words, key=len), directions=directions, inplace=inplace)

    def addwords_recursive(
            self, words, directions, inplace=True, wordsdone=[]):
        if not words:
            self.output(inplace=inplace)
            return True
        numdone = len(wordsdone)
        word = words.pop()
        for r, c, direction in self.product_generator(
                range(self.rows), range(self.cols), directions):
            rstep, cstep = direction
            if self.addword(word, r, c, rstep, cstep, wordsdone):
                status = self.addwords_recursive(
                    words, directions, inplace, wordsdone)
                if inplace and status:
                    return True
                self.clearwords(wordsdone, numdone)
        words.append(word)
        return False

    def addword(self, word, r, c, rstep, cstep, wordsdone=[]):
        """
        rstep, cstep = (0, 1) for across.
        rstep, cstep = (1, 0) for down.
        return whether word was added or not.
        """
        length = str.__len__(word)  # Word must be a string
        lr = r + (length-1) * rstep  # Last row
        lc = c + (length-1) * cstep  # Last column
        if not self.isvalid(lr, lc):
            return False
        if self.checkindex(r - rstep, c - cstep):
            return False
        added_chars = []
        pr = r - cstep  # Previous row
        pc = c - rstep  # Previous column
        nr = r + cstep  # Next row
        nc = c + rstep  # Next column
        for char in word:
            if self[r][c] != self.DEFAULT_CHAR:
                if self[r][c] != char:
                    return False
            elif self.notouch and (
                    self.checkindex(pr, pc) or self.checkindex(nr, nc)):
                return False
            else:
                added_chars.append((r, c, char))
            r, pr, nr = map(rstep.__add__, (r, pr, nr))
            c, pc, nc = map(cstep.__add__, (c, pc, nc))
            # Python needs a more effiecient increment
        if self.checkindex(r, c):
            return False
        for r, c, char in added_chars:
            self[r][c] = char
        wordsdone.append(added_chars)
        return True

    def clearwords(self, wordsdone, leave=0):
        """This modifies wordsdone."""
        for i in range(leave, len(wordsdone)):
            for r, c, char in wordsdone.pop():
                self[r][c] = self.DEFAULT_CHAR

    def isvalid(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def checkindex(self, r, c):
        return self.isvalid(r, c) and self[r][c] != self.DEFAULT_CHAR

"""
words = [
    "ONE",
    "TWO",
    "THREE",
    "FOUR",
    "FIVE",
]

WordGrid(rows=5, cols=5, *words)
"""
