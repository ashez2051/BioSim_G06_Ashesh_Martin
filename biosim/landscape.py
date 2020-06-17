# -*- coding: utf-8 -*-

"""
"""
__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

import numpy as np
import operator
import random
from biosim.fauna import Herbivore, Carnivore


class Landscape:
    """
    Parent class for the landscapes classes water, desert, highland and lowland \n
    """

    parameters = {}

    def __init__(self):
        """
        Constructor for the Landscape class
        """
        self.fauna_dict = {"Herbivore": [], "Carnivore": []}
        self.food_left = 0

    def add_animal(self, animal):
        """
        Adds the animal object to the species dictionary \n
        :param animal: Input animal object \n
        """
        species = animal.__class__.__name__
        self.fauna_dict[species].append(animal)

    def sort_by_fitness(self):
        """
        Sorts the animal by their fitness. Herbivores are sorted from low to high while the \n
        carnivores are sorted from high to low \n
        """
        self.fauna_dict["Herbivore"].sort(key=operator.attrgetter("animal_fitness"))
        self.fauna_dict["Carnivore"].sort(key=operator.attrgetter("animal_fitness"), reverse=True)

    # def update_fodder(self):
    #     """
    #     Method to update fodder in cells, which is overridden in Lowland and Highland \n
    #     """
    #     pass

    def get_fodder(self):
        return self.food_left

    def animal_eats(self):
        """
        The animals in the cells feed, the herbivores feed on fodder and the carnivores \n
        on herbivores \n
        """

        self.herbivore_eats()
        self.carnivore_eats()

    def herbivore_eats(self):
        """
        Herbivores eat randomly, and if there is no fodder available in the cell, the animal \n
        doesn't eat. \n
        If the available fodder is greater than the food the animal requires, \n
        we calculate the food that remains. \n
        If the fodder available is less than the food required by the animal we update remaining \n
        fodder as 0. \n
        """
        self.food_left = self.parameters["f_max"]
        np.random.shuffle(self.fauna_dict["Herbivore"])
        for herb in self.fauna_dict["Herbivore"]:
            if self.food_left <= 0:
                break
            elif self.food_left >= herb.parameters['F']:
                herb.animal_weight_with_food(herb.parameters['F'])
                self.food_left -= herb.parameters['F']
            elif 0 < self.food_left < herb.parameters["F"]:
                herb.animal_weight_with_food(self.food_left)
                self.food_left = 0

    def carnivore_eats(self):
        """
        The carnivores eat in the order of fitness. The carnivore with the highest fitness \n
        eats first and preys on the herbivore with the lowest fitness. If the herbivore is \n
        heavy enough or a carnivore to eat, it eats according to it's appetite, \n
        else it eats the food according to the weight of the herbivore \n
        """
        self.sort_by_fitness()
        for carnivore in self.fauna_dict["Carnivore"]:
            appetite_of_carnivore = carnivore.parameters["F"]
            food_eaten = 0
            dead_animals = []
            for herb in self.fauna_dict["Herbivore"]:

                if np.random.uniform(0, 1) < carnivore.probability_of_killing(herb):
                    if food_eaten < appetite_of_carnivore:
                        eaten = min(carnivore.parameters['F'] - food_eaten, herb.weight)
                        carnivore.animal_weight_with_food(eaten)
                        dead_animals.append(herb)
                        food_eaten += eaten
            self.fauna_dict['Herbivore'] = [herbivore for herbivore in self.fauna_dict['Herbivore']
                                            if herbivore not in dead_animals]

    def update_animal_weight_and_age(self):
        """
        Each year the animals ages by 1 and loses weight by a factor of eta \n
        """
        for species in self.fauna_dict:
            for animal in self.fauna_dict[species]:
                animal.animal_weight_with_age()

    def animal_gives_birth(self):
        """
        Compares the birth_probability of an animal with the randomly generated value between \n
        0 and 1 and if it's greater, the animal gives birth. Creates the child of the same \n
        species and decreases the weight of the animal \n
        """
        for species, animals in self.fauna_dict.items():
            newborns = []
            for animal in animals:
                if animal.proba_animal_birth(len(animals)):
                    child_species = animal.__class__
                    child = child_species()
                    animal.weight_update_after_birth(child)

                    if animal.gives_birth:
                        newborns.append(child)
                        animal.gives_birth = False
            self.fauna_dict[species].extend(newborns)

    # def new_animal_gives_birth(self):
    #     for species, animals in self.fauna_dict.items():
    #         newborns = []
    #         for animal in animals:
    #             child = animal.create_child(len(animals))
    #             if child is not None:
    #                 newborns.append(child)
    #
    #         self.fauna_dict[species].extend(newborns)

    def migration(self, adj_cells):
        """
        Animal can migrate to any of the adjacent cells with equal probability. The animal \n
        is added to the new cell and remove from the old cell. \n
        :param adj_cells: list of adjacent cells that animal can move to \n
        """

        for species, animals in self.fauna_dict.items():
            animals_that_migrated = []
            for animal in animals:
                if animal.has_animal_already_moved is False:
                    if animal.animal_moves_bool:
                        cell_to_migrate = random.choice(adj_cells)
                        if cell_to_migrate.is_migratable:
                            cell_to_migrate.add_animal(animal)
                            animal.has_animal_already_moved = True
                            animals_that_migrated.append(animal)

            self.fauna_dict[species] = [animal for animal in self.fauna_dict[species] if
                                        animal not in animals_that_migrated]

    def reset_migration_bool_in_cell(self):
        """
        Resets the boolean if an animal has moved or not during a year. Ensures that the animal \n
        migrates maximum once per year. \n
        :return: Boolean \n
        """
        for species, animals in self.fauna_dict.items():
            for animal in animals:
                animal.has_animal_already_moved = False

    def animal_dies(self):
        """"
        If the generated random number is greater than the probability of death, we remove \n
        the animal from the dictionary \n
        """
        for species, animals in self.fauna_dict.items():
            dead_animals = []
            for animal in animals:
                if animal.death_probability:
                    dead_animals.append(animal)
            self.fauna_dict[species] = [animal for animal in self.fauna_dict[species] if
                                        animal not in dead_animals]

    @property
    def cell_fauna_count(self):
        """
        Calculates the number of herbivores and carnivores separately \n
        :return: A dictionary with herbivore and carnivore as key and the count as value \n
        """
        herb_count = len(self.fauna_dict['Herbivore'])
        carn_count = len(self.fauna_dict['Carnivore'])
        return {"Herbivore": herb_count, "Carnivore": carn_count}

    @classmethod
    def set_parameters(cls, given_params):
        for param in given_params:
            if param in cls.parameters:
                cls.parameters[param] = given_params[param]
            else:
                raise ValueError('Parameter not set in list' + str(param))
            if cls.parameters["f_max"] < 0:
                raise ValueError("Fodder cannot be negative")


class Water(Landscape):
    """
    Child class of Landscape. Animals are unable to migrate to Water cells \n
    """
    is_migratable = False

    def __init__(self):
        super().__init__()

    def update_fodder(self):
        pass


class Desert(Landscape):
    """
    Child class of Landscape. Animals are able to migrate to Desert cells. \n
    There is no fodder in the desert for herbivores to eat, while carnivores can eat the \n
    herbivores \n
    """
    is_migratable = True

    parameters = {'f_max': 0}

    def __init__(self, given_params=None):
        super().__init__()
        if given_params is not None:
            self.set_parameters(given_params)
        self.food_left = self.parameters['f_max']

    def update_fodder(self):
        pass


class Highland(Landscape):
    """
    Child class of Landscape. Animals are able to migrate to Highland cells. \n
    The amount of fodder is reset every year to the default parameter. Carnivores can \n
    eat the herbivores in the highland \n
    """
    is_migratable = True

    parameters = {'f_max': 300}

    def __init__(self, given_params=None):
        super().__init__()
        if given_params is not None:
            self.set_parameters(given_params)
        self.food_left = self.parameters['f_max']

    def update_fodder(self):
        """
        Updates the amount of fodder back to f_max annually \n
        """
        self.food_left = self.parameters["f_max"]


class Lowland(Landscape):
    """
    Child class of Landscape. Animals are able to migrate to Lowland cells. \n
    The amount of fodder is reset every year to the default parameter. Carnivores can \n
    eat the herbivores in the Lowland. \n
    """

    is_migratable = True

    parameters = {'f_max': 800}

    def __init__(self, given_params=None):
        super().__init__()
        if given_params is not None:
            self.set_parameters(given_params)

        self.food_left = self.parameters['f_max']

    def update_fodder(self):
        """
        Updates the amount of fodder back to f_max annually \n
        """
        self.food_left = self.parameters["f_max"]
