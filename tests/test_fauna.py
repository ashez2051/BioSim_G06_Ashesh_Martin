# -*- coding: utf-8 -*-

"""
Unit tests for methods in fauna.py
"""
__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

import pytest
import numpy as np

from biosim.fauna import Herbivore, Fauna


# Check if it increases with weight
# check if it decreases with age

class TestFauna:
    """Tests for various methods in the fauna class"""

    @pytest.fixture(autouse=True)
    def animal_objects(self):
        self.herb_small = Herbivore(5, 20)
        self.herb_large = Herbivore(5, 50)
        self.herb_young = Herbivore(10, 20)
        self.herb_old = Herbivore(50, 20)

    def test_herb_weight(self):
        """
        Tests if the weight of an animal is larger than zero when its set to 5
        """
        assert self.herb_small.weight > 0

    def test_herb_age(self):
        """
        Tests if the age of an animal is larger than zero when its set to 20
        """
        assert self.herb_small.age > 0

    def test_fitness_between_zero_one(self):
        """
        Tests if the fitness of an animal is between zero and one as specified by the fitness
        function
        """
        assert 0 <= self.herb_small.animal_fitness <= 1

    def test_fitness_increases_with_weight(self):
        """
        Tests if the fitness of an animal increases as their weight increases
        """
        assert self.herb_small.animal_fitness < self.herb_large.animal_fitness
        #fails for some reason

    def test_fitness_decreases_with_age(self):
        assert self.herb_young.animal_fitness > self.herb_old.animal_fitness

    def test_weight_increases_after_eating(self):
        """
        Tests if the weight of an animal that has eaten is larger than the weight
        of an animal that didnt eat
        """
        assert self.herb_small.animal_weight_with_food(0) < \
               self.herb_small.animal_weight_with_food(10)

    def test_age_equals_zero_when_born(self):
        pass

    def test_weight_decreases_at_end_of_the_year(self):
        pass

    def test_age_increases_by_one_per_year(self):
        """
        Takes an animal with age 5 in this case. Then loops for 2 years and the animal
        should then be 7 years old
        """
        for _ in range(2):
            self.herb_small.animal_weight_with_age()
        assert self.herb_small.age == 7


    def test_no_birth_when_mother_loses_more_than_her_weight(self):
        pass






