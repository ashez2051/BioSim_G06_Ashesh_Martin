# -*- coding: utf-8 -*-

"""
"""
__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

import numpy as np
from numba import njit


class Fauna:
    """
    Parent class for the herbivores and carnivores
    """

    parameters = {}

    def __init__(self, age=None, weight=None):
        """
        Constructor for the parent class fauna with age and weight of the animals \n
        :param age: Age of the animal, integer \n
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
        #self.gives_birth = False
        self.has_animal_already_moved = False

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
        self.age += 1
        self.weight -= self.parameters['eta'] * self.weight

    def animal_weight_with_food(self, food_eaten):
        """
        Updates the weight of an animal based on it's feeding behavior \n
        :param food_eaten: the amount of food eaten by an animal, float
        """
        self.weight += self.parameters['beta'] * food_eaten
        return self.weight

    @property
    # @njit(parallel=True, fastmath=True)
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

    # def proba_animal_birth(self, num_animals):
    #     """
    #     Calculates the probability for an animal to give birth \n
    #     :param num_animals: Number of animals of the same species in a single cell \n
    #     :return: true/False probability of giving birth
    #     """
    #
    #     weight_check = self.parameters["zeta"] * (
    #             self.parameters["w_birth"] + self.parameters["sigma_birth"])
    #
    #     if num_animals >= 2 and self.weight > weight_check:  # Removed equal in >=
    #         return np.random.uniform(0, 1) < min(1, (
    #                 self.parameters["gamma"] * self.animal_fitness * (num_animals - 1)))
    #     else:
    #         return False
    #
    # def weight_update_after_birth(self, child):
    #     """
    #     Update the weight of the mother after giving birth and determines if the animal will \n
    #     give birth. If the weight of the child times xi is larger than the weight of the mother \n
    #     the animal wont give birth \n
    #     :param child: The child object
    #     """
    #     if self.weight > child.weight * child.parameters["xi"]:
    #         self.weight -= child.weight * child.parameters["xi"]
    #         self.gives_birth = True
    #     else:
    #         self.gives_birth = False

    def check_mating_weight_conditions(self, num_animals):
        if num_animals >= 2:
            weight_condition = self.parameters['zeta'] * (
                    self.parameters['w_birth'] + self.parameters['sigma_birth'])
            if self.weight > weight_condition:
                return True
            else:
                return False
        else:
            return False

    def check_mother_minus_newborn_weight_conditions(self, child_weight):
        if self.weight >= self.parameters['xi'] * child_weight:
            # Reduce weight of mother by the weight of child * xi
            self.weight -= self.parameters['xi'] * child_weight
            return True
        else:
            return False

    def create_child(self, num_animals):
        if self.check_mating_weight_conditions(num_animals):
            prob = min(1, self.parameters['gamma'] * self.animal_fitness * (num_animals - 1))
            bool_value = np.random.uniform(0, 1) < prob
            if bool_value:
                child = self.__class__()
                if self.check_mother_minus_newborn_weight_conditions(child.weight):
                    return child
            else:
                return None

    @property
    def death_probability(self):
        """
        Calculates the probability of death based on fitness \n
        :return: Boolean value weather an animal dies or survives
        """
        if self.animal_fitness <= 0:
            return True
        else:
            return np.random.uniform(0, 1) < self.parameters['omega'] * (1 - self.animal_fitness)

    @property
    def animal_moves_bool(self):
        """
        Calculates the probability that an animal moves \n
        :return: Boolean if an animal moves or not
        """
        moving_probability = self.parameters["mu"] * self.animal_fitness
        return np.random.uniform(0, 1) < moving_probability

    @classmethod
    def set_parameters(cls, given_params):
        """
        Sets the parameters according to the class called \n
        :param given_params: a dictionary of the user assigned parameters \n
        :return: Assigns parameters to respective classes
        """
        for param in given_params:
            if param in cls.parameters:
                if given_params[param] < 0:
                    raise ValueError('Parameter value should be positive ')
                else:
                    cls.parameters[param] = given_params[param]
                if cls.parameters["eta"] >= 1:
                    raise ValueError("eta has to be equal to or less than 1")
            else:
                raise ValueError("Parameter not in class parameter list")


class Herbivore(Fauna):
    """
    Child class of Fauna defined with default parameter values
    """
    parameters = {"w_birth": 8.0, "sigma_birth": 1.5, "beta": 0.9, "eta": 0.05, "a_half": 40.0,
                  "phi_age": 0.6, "w_half": 10.0, "phi_weight": 0.1, "mu": 0.25, "gamma": 0.2,
                  "zeta": 3.5, "xi": 1.2, "omega": 0.4, "F": 10.0}

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)
        self.parameters = Herbivore.parameters
        if self.weight < 0:
            raise ValueError("Weight cannot be negative")
        if self.age < 0:
            raise ValueError("Age cannot be negative")


class Carnivore(Fauna):
    """
    Child class of Fauna defined with default parameter values
    """
    parameters = {"w_birth": 6.0, "sigma_birth": 1, "beta": 0.75, "eta": 0.125, "a_half": 40.0,
                  "phi_age": 0.3, "w_half": 4.0, "phi_weight": 0.4, "mu": 0.4, "gamma": 0.8,
                  "zeta": 3.5, "xi": 1.1, "omega": 0.8, "F": 50.0, "DeltaPhiMax": 10.0}

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)
        self.parameters = Carnivore.parameters
        if self.weight < 0:
            raise ValueError("Weight cannot be negative")
        if self.age < 0:
            raise ValueError("Age cannot be negative")

    # @njit(parallel=True, fastmath=True)
    def probability_of_killing(self, herb):
        """"
        Returns the probability with which a carnivore kills a herbivore \n
        If the fitness of the carnivore is less than that of a herbivore we return 0 \n
        If the difference in fitness is > 0 and < delta_phi_max then it is calculated \n
        as (difference / delta_phi_max) \n
        :param herb: Herbivore class object \n
        :return: probability value
        """
        if self.parameters["DeltaPhiMax"] <= 0:
            raise ValueError("DeltaPhiMax must be strictly positive")
        else:
            if self.animal_fitness <= herb.animal_fitness:
                return 0
            elif 0 < (self.animal_fitness - herb.animal_fitness) < self.parameters["DeltaPhiMax"]:
                return (self.animal_fitness - herb.animal_fitness) / self.parameters["DeltaPhiMax"]
            else:
                return 1
