# -*- coding: utf-8 -*-

"""
Unit tests for methods in fauna.py
"""
__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

import pytest
import numpy as np

from biosim.fauna import Herbivore, Fauna

animal = Fauna(age=5, weight=20)


class TestFauna:
    """Tests for various methods in the fauna class"""

    @pytest.fixture(autouse=True)
    def animal_objects(self):
        np.random.seed(123)
        herb = Herbivore()
        return herb



    def test_weight_larger_than_zero(simple_herbivore):
        assert bbbbbbbbbbbbbbbb.weight > 0

