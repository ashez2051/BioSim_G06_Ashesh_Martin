# -*- coding: utf-8 -*-

"""
Island class which gives a geographical structure of the multiline string provided.
Returns a numpy array with cell information equal to the number of characters in given string
"""
__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

from biosim.landscape import *


class Island:
    """
    This class represents the given map string as an array of objects
    """

    def __init__(self, island_map):
        self.island_map = island_map
        self.island_map = self.string_to_array()
        self.check_surrounded_by_ocean(self.island_map)

        self.landscape_dict = {'W': Water, 'D': Desert, 'L': Lowland, 'H': Highland}

        self._cells = self.create_array_with_landscape_objects()

        rows = self._cells.shape[0]
        cols = self._cells.shape[1]
        self.map_dims = rows, cols

    @property
    def cells(self):
        """
         :return: landscape objects
        """
        return self._cells

    def string_to_array(self):
        """
        Gets numpy array from multidimensional string
        """
        map_str_clean = self.map.replace(' ', '') ## necessary?
        char_map = np.array([[col for col in row] for row in map_str_clean.splitlines()])
        return char_map
