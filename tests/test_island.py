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


class TestIsland:
    def test_string_to_array(self):
        """
        testing the string_to_array method by verifying the individual cell
        and also by looking at the type of output
        """
        map_str = """   WWW
                        WLW
                        WWW"""
        island = Island(map_str)
        assert island.convert_string_to_array()[0][0] == 'W'
        assert island.convert_string_to_array()[1][1] == 'L'
        assert type(island.convert_string_to_array()).__name__ == 'ndarray'

    def test_create_array_with_landscape_objects(self):
        map_str = """   WWW
                        WLW
                        WWW"""
        island = Island(map_str)
        assert isinstance(island.array_with_landscape_objects()[0][0], Water)
        assert isinstance(island.array_with_landscape_objects()[1][1], Lowland)

    def test_adjacent_cells(self):
        map_str = """   WWW
                        WLW
                        WWW"""
        island = Island(map_str)
        island.convert_string_to_array()
        #for cells in island.adjacent_cells(0,0):
            #assert cells == [W(), W()]
        assert all(j in island.adjacent_cells(0, 0) for j in ['W', 'W']) ### Check for help

    def test_check_surrounded_by_water(self):
        """
        verifying if value error is raised when edges dont contain water cells
        """
        map_str = """   LLL
                        LLL
                        LLL"""
        with pytest.raises(ValueError) as err:
            Island(map_str)
            assert err.type is ValueError

    def test_add_animals(self):
        """
        Testing add_animals and total_animals_per_species methods
        """
        map_str = """   WWWWWW
                        WHLLHW
                        WLLLLW
                        WWWWWW"""

        island = Island(map_str)
        ini_pop = [{"loc": (1, 1), "pop": [{"species": "Herbivore", "age": 5, "weight": 20},
                                           {"species": "Herbivore", "age": 5, "weight": 20},
                                           {"species": "Carnivore", "age": 5, "weight": 20}]},
            {"loc": (1, 2), "pop": [{"species": "Herbivore", "age": 5, "weight": 20},
                                    {"species": "Carnivore", "age": 5, "weight": 20}]}]

        island.add_animals(ini_pop)
        assert island.number_of_animals_per_species('Herbivore') == 3
        assert island.number_of_animals_per_species('Carnivore') == 2


def test_animal_migrates_maximum_once_per_year(self):
    pass


def test_equal_probability_of_migration_to_each_cell(self):
    pass


def test_animals_cannot_migrate_in_water(self):
    pass
