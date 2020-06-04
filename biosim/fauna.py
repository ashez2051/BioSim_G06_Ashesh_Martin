# -*- coding: utf-8 -*-

"""
"""
__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

import numpy as np
import math


class Fauna:
    """
    Parent class for the herbivores and carnivores
    """

    parameters = {}

    def __init__(self, age=None, weight=None):
        """
        Constructor for the parent class fauna with age and weight of the animals
        :param age: Age of the animal, integer
        :param weight: Weight of the animal, float
        """
        if age is None:
            self.age = 0
        else:
            self.age = age
        if weight is None:
            self.weight = np.random.normal(self.parameters["w_birth"],
                                           self.parameters["sigma_birth"])
        else:
            self.weight = weight
        # Define "things" that applies for both animals
        self.fitness = 0
        self.gives_birth = False

    @property
    def animal_weight(self):
        """
        :return: weight of the animal
        """
        return self.weight

    def animal_weight_with_age(self):
        """
        Updates the age of an animal and it's weight at the end of the year
        """
        self.weight = self.parameters['eta'] * self.weight
        self.age += 1

    def animal_weight_with_food(self, food_eaten):
        """
        Updates the weight of an animal based on it's feeding behavior
        :param food_eaten: the amount of food eaten by an animal, float
        """
        self.weight += self.parameters['beta'] * food_eaten

    @property
    def animal_fitness(self):
        """"
        Calculates the fitness of an animal based on age and weight
        """
        if self.weight > 0:
            q_pos = 1/(1+np.exp(self.parameters['phi_age'] *
                                (self.age - self.parameters['a_half'])))

            q_neg = 1/(1+ np.exp(self.parameters['phi_weight'] *
                                 (self.weight - self.parameters['w_half'])))

            return q_neg * q_pos
        else:
            return 0
        



class Herbivore(Fauna):
    """
    Child class of Fauna
    """
    parameters = {"w_birth": 8.0, "sigma_birth": 1.5, "beta": 0.9, "eta": 0.05, "a_half": 40.0,
                  "phi_age": 0.6, "w_half": 10.0, "phi_weight": 0.1, "mu": 0.25, "lambda": 1.0,
                  "gamma": 0.2, "zeta": 3.5, "xi": 1.2, "omega": 0.4, "F": 10.0}

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)
        self.parameters = Herbivore.parameters


class Carnivore(Fauna):
    """
    Child class of Fauna
    """
    parameters = {}

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)
        self.parameters = Carnivore.parameters
