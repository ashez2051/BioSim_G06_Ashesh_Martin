# -*- coding: utf-8 -*-

"""
Unit tests for methods in island.py
"""
__author__ = "Ashesh Raj Gnawali, Martin Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

import pytest
import numpy as np

from biosim.island import *
from biosim.fauna import *
from biosim.landscape import Landscape, Lowland, Water, Highland, Desert


class TestIsland:
    def test_string_to_array(self):
        """
        testing the string_to_array method by verifying the individual cell
        and also by looking at the type of output in specific cells
        """
        map_str = """   WWW
                        WLW
                        WWW"""
        island = Island(map_str)
        assert island.convert_string_to_array()[0][0] == 'W'
        assert island.convert_string_to_array()[1][1] == 'L'
        assert type(island.convert_string_to_array()).__name__ == 'ndarray'

    def test_create_array_with_landscape_objects(self):
        """
        Test that a landscape object is being created with the array_with_landscape_object \n
        function with isinstance
        """
        map_str = """   WWW
                        WLW
                        WWW"""
        island = Island(map_str)
        assert isinstance(island.array_with_landscape_objects()[0][0], Water)
        assert isinstance(island.array_with_landscape_objects()[1][1], Lowland)

    def test_adjacent_cells(self):
        """
        Test if the adjacent cells of the top left cell is water
        """
        map_str = """   WWW
                        WLW
                        WWW"""
        island = Island(map_str)
        for cells in island.adjacent_cells(0, 0):
            assert type(cells) == type(Water())

    def test_check_surrounded_by_water(self):
        """
        Testing if value error is raised when edges dont contain water cells
        """
        map_str = """   LLL
                        LLL
                        LLL"""
        with pytest.raises(ValueError) as err:
            Island(map_str)
            assert err.type is ValueError

    def test_add_animals(self):
        """
        Testing add_animals and total_animals_per_species methods in the island class
        """
        map_str = """   WWWWWWWWWWWW
                        WHLWWWWWDHLW
                        WWWWWWWWWWWW"""
        island = Island(map_str)

        animals = [{"loc": (2, 2), "pop": [{"species": "Herbivore", "age": 10, "weight": 10.0},
                                           {"species": "Carnivore", "age": 11,
                                            "weight": 11.0}, ], },

                   {"loc": (2, 3), "pop": [{"species": "Herbivore", "age": 10, "weight": 10.0},
                                           {"species": "Herbivore", "age": 11, "weight": 11.0},
                                           {"species": "Carnivore", "age": 12,
                                            "weight": 12.0}, ], }, ]
        island.add_animals(animals)
        assert island.number_of_animals_per_species('Herbivore') == 3
        assert island.number_of_animals_per_species('Carnivore') == 2

    def test_valueerror_when_placed_in_water(self):
        """
        Testing add_animals and total_animals_per_species methods in the island class
        """
        map_str = """   WWWWWWWWWWWW
                        WHLWWWWWDHLW
                        WWWWWWWWWWWW"""
        island = Island(map_str)

        animals = [{"loc": (1, 1), "pop": [{"species": "Herbivore", "age": 10, "weight": 10.0},
                                           {"species": "Carnivore", "age": 11,
                                            "weight": 11.0}, ], }]
        with pytest.raises(ValueError) as err:
            island.add_animals(animals)
            assert err.type is ValueError
