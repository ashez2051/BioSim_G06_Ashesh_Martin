# -*- coding: utf-8 -*-

"""
Unit tests for methods in fauna.py
"""
__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

import pytest
from biosim.fauna import Herbivore, Carnivore
import math
import scipy.stats as stats
from scipy.stats import binom_test

ALPHA = 0.01


class TestFauna:
    """
    Tests for various methods in the fauna class \n
    """

    @pytest.fixture(autouse=True)
    def animal_objects(self):
        self.herb_small = Herbivore(5, 20)
        self.herb_large = Herbivore(5, 50)
        self.herb_young = Herbivore(10, 20)
        self.herb_old = Herbivore(50, 20)
        self.herb_no_weight = Herbivore(20, 0)
        self.herb = Herbivore()

        self.carn_small = Carnivore(5, 20)
        self.carn_large = Carnivore(5, 50)
        self.carn_young = Carnivore(10, 20)
        self.carn_old = Carnivore(50, 20)
        self.carn = Carnivore()

    def test_animal_weight(self):
        """
        Tests if the weight of an animal is larger than zero when its set to 5 \n
        """
        assert self.herb_small.weight > 0
        assert self.carn_small.weight > 0

    def test_herb_age(self):
        """
        Tests if the age of an animal is larger than zero when its set to 20 \n
        """
        assert self.herb_small.age > 0
        assert self.carn_small.age > 0

    def test_fitness_between_zero_one(self):
        """
        Tests if the fitness of an animal is between zero and one as specified by the fitness \n
        function \n
        """
        assert 0 <= self.herb_small.animal_fitness <= 1
        assert 0 <= self.carn_small.animal_fitness <= 1

    def test_fitness_increases_with_weight(self):
        """
        Tests if the fitness of an animal increases as their weight increases \n
        """
        assert self.herb_small.animal_fitness < self.herb_large.animal_fitness
        assert self.carn_small.animal_fitness < self.carn_large.animal_fitness

    def test_fitness_decreases_with_age(self):
        """
        Tests if the animal fitness decreases with age. Assumption is that a young animal \n
        will have better fitness than an older animal assuming equal weight. \n
        """
        assert self.herb_young.animal_fitness > self.herb_old.animal_fitness
        assert self.carn_young.animal_fitness > self.carn_old.animal_fitness

    def test_weight_increases_after_eating(self):
        """
        Tests if the weight of an animal that has eaten is larger than the weight \n
        of an animal that didnt eat \n
        """
        assert self.herb_small.animal_weight_with_food(0) < self.herb_small.animal_weight_with_food(
            10)
        assert self.carn_small.animal_weight_with_food(0) < self.carn_small.animal_weight_with_food(
            10)

    def test_probability_of_birth_if_only_one_animal(self):
        """
        Testing probability of birth returns False when only \n
        one animal is present \n
        """
        assert self.herb_small.proba_animal_birth(1) is False
        assert self.carn_young.proba_animal_birth(1) is False

    def test_probability_of_birth_for_more_than_two_animal(self):
        """
        Checks the probability of birth when more than 2 animals exists \n
        """
        assert self.herb_small.proba_animal_birth(20) is False
        assert self.carn_young.proba_animal_birth(10) is False

    def test_age_increases_by_one_per_year(self):
        """
        Takes an animal with age 5 in this case. Then loops for 2 years and the animal \n
        should then be 7 years old \n
        """
        for _ in range(2):
            self.herb_small.animal_weight_with_age()
            self.carn_small.animal_weight_with_age()
        assert self.herb_small.age == 7
        assert self.carn_small.age == 7

    def test_weight_decreases_at_end_of_the_year(self):
        """
        Tests if the weight of an animal is decreased after one year \n
        """
        weight_before = self.herb_small.weight
        for _ in range(1):
            self.herb_small.animal_weight_with_age()
        assert self.herb_small.weight < weight_before

    def test_animal_dies(self):
        """
        test that animal dies when it's weight/fitness is 0 \n
        """
        self.herb.weight = 0
        assert self.herb.death_probability is True

    def test_animal_migration_chances(self, mocker):
        """
        test that the bool of migration is False if \n
        weight/ fitness is zero \n
        """
        mocker.patch('numpy.random.uniform', return_value=0)
        self.carn_young.weight = 0
        assert self.carn_young.animal_moves_bool is False

    def test_animal_migration_chances_for_fit_animal(self, mocker):
        """
        test the probability of migration is True if \n
        fitness is high \n
        """
        mocker.patch('numpy.random.uniform', return_value=0)
        assert self.herb_young.animal_moves_bool

    def test_carnivore_kills(self, mocker):
        """
        Test that carnivore kills herbivore if carnivore fitness is greater than \n
        herbivore fitness. \n
        """
        mocker.patch('numpy.random.uniform', return_value=0)
        assert self.carn_young.probability_of_killing(self.herb_old)

    def test_valueerror_for_negative_age(self):
        """
        Tests if valueerror is being raised when a negative age is set as input
        """
        with pytest.raises(ValueError) as err:
            Herbivore(-5, 20)
            assert err.type is ValueError

    def test_valueerror_for_negative_weight(self):
        """
        Tests if value error is being raised when a negative weight is set as input
        """
        with pytest.raises(ValueError) as err:
            Herbivore(5, -20)
            assert err.type is ValueError

    def test_death_z_test(self, mocker):

        """
        Probabilistic test of death function. Test the number of deaths is
        normally distributed for large number of animals. And the death probability is
        significant with a p-value of 0.01.
        : param p: The hypothesized probabilty
        """
        mocker.patch("biosim.fauna.Fauna.death_probability", return_value=0.1)
        hypo_proba = 0.1
        num_animals = 100
        n_died = sum(self.herb_small.death_probability() for _ in range(num_animals))
        mean = num_animals * hypo_proba
        var = num_animals * hypo_proba * (1 - hypo_proba)
        z = (n_died - mean) / math.sqrt(var)
        phi = 2 * stats.norm.cdf(-abs(z))
        assert phi > ALPHA

    def test_bionmial_death(self, mocker):
        """
        Test if the death function returns statistical significant results
        under the bionomial test, with a given death probability p.
        : param p: The hypothesized probabilty
        """
        mocker.patch("biosim.fauna.Fauna.death_probability", return_value=0.5)
        hypo_proba = 0.5
        num_animals = 100
        num_dead = sum(self.carn_large.death_probability() for _ in range(num_animals))
        assert binom_test(num_dead, num_animals, hypo_proba) > ALPHA
