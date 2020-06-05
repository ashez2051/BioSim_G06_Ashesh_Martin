__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"


class Landscape:
    """
    Parent class for various landscapes water, desert, highland and lowland
    """

    def __init__(self):
        self.sorted_animal_fitness_dict = {} #needed for when we introduce carnivores
        self.fauna_dict = {"Hebivore": []} # Add carnivore later
        self.updated_fauna_dict = {"Hebivore": []} # Add carnivore later
        self._reset_remaining_food = {'Herbivore': 0, 'Carnivore': 0} #might need to have the same name as the method remaining_food


    def add_animal(self, animal):
        """
        Adds the animal object to the species list of cell
        :param animal: Input animal object, Herbivore or Carnivore
        """
        species = animal.__class__.__name__
        self.fauna_dict[species].append(animal)


    def remove_animal(self, animal):
        """
        Removes the animal object from the list of species of cell
        :param animal: Input animal object, Herbivore or Carnivore
        :return:
        """
        species = animal.__class__.__name__
        self.fauna_dict[species].remove(animal)

    def store_fitness(self):
        pass


    def animal_eats(self):
        pass

    def herbivore_eats(self):
        pass

    def update_fodder(self):
        pass

    def update_animal_weight(self):
        pass

    def animal_gives_birth
        pass

    def add_children_to_adult_animals(self):
        pass

    def animal_dies(self):
        pass

    def grow_all_animals(self): #aging?
        pass

    def cell_fauna_count(self):
        pass

    def total_hebivore_weight(self): #not needed before we introduce carnivores
        pass

    def remaining_food(self):
        pass


class Water(Landscape):
    def __init__(self):
        pass


class Desert(Landscape):
    def __init__(self):
        pass


class Highland(Landscape):
    def __init__(self):
        pass


class Lowland(Landscape):
    def __init__(self):
        pass
