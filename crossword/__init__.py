"""Crossword and Wordsearch creator on the fly."""

import itertools

from wordgrid import WordGrid, RandomProduct


class Crossword(WordGrid):
    DEFAULT_CHAR = "*"
    directions = [
        (0, +1),  # Across
        (+1, 0),  # Down
    ]
    product_generator = itertools.product
    notouch = True


class Wordsearch(WordGrid):
    DEFAULT_CHAR = "*"
    directions = [
        (0, +1),  # Across
        (+1, 0),  # Down
        (0, -1),  # Backwards
        (-1, 0),  # Up
        (+1, +1),  # Diagonal bottom-right
        (+1, -1),  # Diagonal bottom-left
        (-1, +1),  # Diagonal top-right
        (-1, -1),  # Diagonal top-left
    ]
    product_generator = RandomProduct
    notouch = False


"""
endangered_species = '''
ASIANELEPHANT
AXOLOTL
BLUEWHALE
CHIMPANZEE
GHARIAL
HUMAN
JAVANRHINOCEROS
KINGCOBRA
KOALA
KOMODODRAGON
LEOPARD
LION
PUFFERFISH
PYGMYRACCOON
REDPANDA
TIGER
'''
words = endangered_species.strip('\n').split("\n")

crossword = Crossword(15, 15)
crossword.addwords(*words, inplace=False)
"""
