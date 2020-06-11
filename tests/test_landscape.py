import pytest


from biosim.landscape import Landscape, Lowland, Water, Highland, Desert
from biosim.fauna import Herbivore, Carnivore


class TestLandscape:

    @pytest.fixture(autouse=True)
    def animal_objects(self):
        self.herb1 = Herbivore()
        self.herb2 = Herbivore()
        self.carn1 = Carnivore()
        self.carn2 = Carnivore()
        return self.herb1,self.herb2, self.carn1, self.carn2

    @pytest.fixture
    def landscape_data(self, animal_objects):
        herb1, herb2, carn1, carn2 = animal_objects
        animals = {'Herbivore': [herb1, herb2], 'Carnivore': [carn1, carn2]}

        landscapes_dict = {'W': Water(), 'H': Highland(), 'L': Lowland(), 'D': Desert()}
        for species, animals in animals.items():
            for animal in animals:
                landscapes_dict['L'].add_animal(animal)
                landscapes_dict['D'].add_animal(animal)
                landscapes_dict['H'].add_animal(animal)
        return landscapes_dict

    def test_add_animals(self, landscape_data):
        lowland = landscape_data["L"]
        assert len(lowland.fauna_dict['Herbivore']) == 2
        herb3 = Herbivore()
        lowland.add_animal(herb3)
        assert len(lowland.fauna_dict['Herbivore']) == 3

    def test_remove_animals(self, landscape_data):
        lowland = landscape_data["L"]
        assert len(lowland.fauna_dict['Herbivore']) == 2
        lowland.remove_animal(self.herb1)
        assert len(lowland.fauna_dict['Herbivore']) == 1

    def test_herbivore_eats_in_lowland(self, landscape_data):
        lowland = landscape_data['L']
        self.herb1 = lowland.fauna_dict['Herbivore'][0]
        herb1_weight_before_eat = self.herb1.weight
        lowland.animal_eats()
        herb1_weight_after_eat = self.herb1.weight
        assert herb1_weight_after_eat >= herb1_weight_before_eat

    def test_carnivore_eats_herbivore_in_lowland(self, landscape_data):
        pass

    def test_place_carn_and_herb_in_cell(self):
        pass

    def test_animals_cannot_migrate_in_water(self):
        pass

    def test_herbivore_doesnt_eat_in_the_desert(self):
        pass

    def test_place_carn_in_cell_without_food(self):
        """
        Check if they all die
        :return:
        """
        pass

    def test_equal_probability_of_migration_to_each_cell(self):
        pass

    def test_resets_fodder_each_year(self):
        pass

    def test_animal_count_reduces_when_animal_dies(self):
        pass

    def test_animal_count_increases_when_animal_is_born(self):
        pass

    def test_calculation_of_total_herbivore_weight(self):
        pass

    def test_remaining_food_for_herbs_is_correctly_calculated(self):
        pass

    #Statistical tests
    #Things that has to do with probability

    def test_order_by_fitness(self):
        pass

    def test_animal_migrates_maximum_once_per_year(self):
        pass

    def test_carnivore_eats_least_fit_herbivore(self):
        pass




