# -*- coding: utf-8 -*-

"""
"""
__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

import numpy as np
import math

np.random.seed(123)


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
        return self.weight

    @property
    def animal_fitness(self):
        """"
        Calculates the fitness of an animal based on age and weight
        """
        if self.weight > 0:
            q_pos = 1 / (1 + np.exp(
                self.parameters['phi_age'] * (self.age - self.parameters['a_half'])))

            q_neg = 1 / (1 + np.exp(
                -1 * self.parameters['phi_weight'] * (self.weight - self.parameters['w_half'])))

            return q_neg * q_pos
        else:
            return 0

    def proba_animal_birth(self, num_animals):
        """
        Calculates the probability for an animal to give birth
        :param num_animals: Number of animals of the same species in a single cell
        :return: probability of giving birth

        """
        weight_check = self.parameters["zeta"] * (
                self.parameters["w_birth"] + self.parameters["sigma_birth"])

        if num_animals >= 2 and self.weight >= weight_check:
            return np.random.uniform(0, 1) < min(1, (
                    self.parameters["gamma"] * self.animal_fitness * (num_animals - 1)))

    def weight_update_after_birth(self, child):
        """
        Update the weight of the mother after giving birth
        :return:
        """
        if self.weight > child.weight * child.parameters["xi"]:
            self.weight -= child.weight * child.parameters[
                "xi"]  # Add self.gives_birth or something later

    def death_probability(self):
        """
        Calculates the probability of death based on fitness
        :return: Boolean value weather an animal dies or survives
        """
        if self.animal_fitness == 0:
            return False
        else:
            return np.random.uniform(0, 1) < self.parameters['omega'] * (1 - self.animal_fitness)

    @property
    def probablity_of_moving(self):
        pass

    @classmethod
    def set_parameters(cls, given_params):
        """
        Sets the parameters according to the class called
        :param given_params: a dictionary of the user assigned parameters
        :return: Assigns parameters to respective classes
        """
        for param in given_params:
            if param in cls.parameters:
                if given_params[param] <= 0:
                    raise ValueError('Parameter value should be positive ')
                else:
                    cls.parameters[param] = given_params[param]
            else:
                raise ValueError("Parameter not in class parameter list")


class Herbivore(Fauna):
    """
    Child class of Fauna
    """
    parameters = {"w_birth": 8.0, "sigma_birth": 1.5, "beta": 0.9, "eta": 0.05, "a_half": 40.0,
                  "phi_age": 0.6, "w_half": 10.0, "phi_weight": 0.1, "mu": 0.25, "gamma": 0.2,
                  "lambda": 1, "zeta": 3.5, "xi": 1.2, "omega": 0.4, "F": 10.0}

    def __init__(self, age=None, weight=None):
        super().__init__(age,
                         weight)  # self.parameters = Herbivore.parameters Dont need this, defined in the self


class Carnivore(Fauna):
    """
    Child class of Fauna
    """
    parameters = {"w_birth": 6.0, "sigma_birth": 1, "beta": 0.75, "eta": 0.125, "a_half": 40.0,
                  "phi_age": 0.3, "w_half": 4.0, "phi_weight": 0.4, "mu": 0.4, "gamma": 0.8,
                  "lambda": 1, "zeta": 3.5, "xi": 1.1, "omega": 0.8, "F": 50.0,
                  "delta_phi_max": 10.0}

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)  # self.parameters = Carnivore.parameters

    def probability_of_killing(self, herb):
        """"
        Returns the probability with which a carnivore kills a herbivore
        If the fitness of the carnivore is less than that of a herbivore we return 0
        If the difference in fitness is > 0 and < delta_phi_max then it is calculated
        as (difference / delta_phi_max)
        :param herb: Herbivore class object
        :return: probability value
        """
        pass
