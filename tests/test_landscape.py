import pytest

from biosim.landscape import Landscape, Lowland, Water, Highland, Desert
from biosim.fauna import Herbivore, Carnivore
import os

class TestLandscape:

    @pytest.fixture(autouse=True)
    def animal_objects(self):
        self.herb1 = Herbivore(10, 50)
        self.herb2 = Herbivore(20, 35)
        self.carn1 = Carnivore(5, 60)
        self.carn2 = Carnivore(20, 40)
        return self.herb1, self.herb2, self.carn1, self.carn2

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
        assert herb1_weight_after_eat > herb1_weight_before_eat

    def test_carnivore_eats_herbivore_in_lowland(self, landscape_data, mocker):
        mocker.patch("numpy.random.uniform", return_value = 0)
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        self.carn1 = lowland.fauna_dict["Carnivore"][0]
        weight_before = self.carn1.weight
        lowland.carnivore_eats()
        assert self.carn1.weight > weight_before  ### Ask for help


    def test_place_carn_and_herb_in_cell(self, landscape_data):
        lowland = landscape_data["L"]
        count = lowland.cell_fauna_count
        assert count['Herbivore'] == 2 and count["Carnivore"] == 2


    def test_herbivore_doesnt_eat_in_the_desert(self, landscape_data):
        desert = landscape_data["D"]
        self.herb1 = desert.fauna_dict['Herbivore'][0]
        herb1_weight_before_eat = self.herb1.weight
        herb1_fitness_before_eat = self.herb1.animal_fitness
        desert.animal_eats()
        herb1_weight_after_eat = self.herb1.weight
        herb1_fitness_after_eat = self.herb1.animal_fitness

        assert herb1_weight_after_eat == herb1_weight_before_eat
        assert herb1_fitness_after_eat == herb1_fitness_before_eat

    def test_place_carn_in_cell_without_food(self, landscape_data):
        """
        Check if they all die
        """
        highland = landscape_data["H"]
        self.carn1 = highland.fauna_dict["Carnivore"][0]
        weight_before = self.carn1.weight
        highland.animal_eats()
        weight_after = self.carn1.weight
        assert weight_before == weight_after



    def test_resets_fodder_each_year(self, landscape_data):
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        for _ in range(10):
            lowland.animal_eats()
            lowland.update_fodder()
        assert lowland.remaining_food["Herbivore"] == 800

    def test_herb_count_reduces_when_herb_gets_eaten(self, landscape_data, mocker):
        """
        This test might not pass always because of the probability 
        """""
        mocker.patch("numpy.random.uniform", return_value = 0)
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        self.herb2 = lowland.fauna_dict["Herbivore"][1]
        self.carn1 = lowland.fauna_dict["Carnivore"][0]
        self.carn2 = lowland.fauna_dict["Carnivore"][1]
        initial_herb_count = lowland.cell_fauna_count['Herbivore']
        initial_carn_count = lowland.cell_fauna_count["Carnivore"]

        lowland.carnivore_eats()

        assert lowland.cell_fauna_count["Herbivore"] == 0


    def test_animal_count_increases_when_animal_is_born(self, landscape_data, mocker):
        #mocker.patch("landscape.proba_animal_birth", return_value = True)
        #Didnt find the path, will work on this later
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        self.herb2 = lowland.fauna_dict["Herbivore"][1]
        initial_count = lowland.cell_fauna_count["Herbivore"]
        self.herb1.proba_animal_birth(2)
        lowland.animal_gives_birth()
        lowland.add_children_to_adult_animals()
        assert initial_count <= lowland.cell_fauna_count["Herbivore"]


    def test_calculation_of_total_herbivore_weight(self, landscape_data):
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        self.herb2 = lowland.fauna_dict["Herbivore"][1]
        assert lowland.total_herbivore_weight() == (self.herb1.weight + self.herb2.weight)



    def test_remaining_food_for_herbs_is_correctly_calculated(self, landscape_data):
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        lowland.herbivore_eats()



    # Statistical tests
    # Things that has to do with probability

    def test_sort_by_fitness_herb(self, landscape_data):
        lowland = landscape_data['L']
        lowland.sort_by_fitness()
        self.herb1 = lowland.fauna_dict['Herbivore'][0]
        self.herb2 = lowland.fauna_dict['Herbivore'][1]
        assert self.herb1.animal_fitness < self.herb2.animal_fitness

    def test_sort_by_fitness_carn(self, landscape_data):
        lowland = landscape_data['L']
        lowland.sort_by_fitness()
        self.carn1 = lowland.fauna_dict['Carnivore'][0]
        self.carn2 = lowland.fauna_dict['Carnivore'][1]
        assert self.carn1.animal_fitness > self.carn2.animal_fitness


    def test_carnivore_eats_least_fit_herbivore(self, landscape_data, mocker):
        mocker.patch("numpy.random.uniform", return_value=0)
        lowland = landscape_data['L']
        self.herb1 = lowland.fauna_dict['Herbivore'][0]
        self.herb2 = lowland.fauna_dict['Herbivore'][1]

        self.carn1 = lowland.fauna_dict['Carnivore'][0]
        lowland.sort_by_fitness()
        herb1_fitness = self.herb1.animal_fitness
        herb2_fitness = self.herb2.animal_fitness
        assert herb1_fitness > herb2_fitness
        lowland.carnivore_eats()
        assert self.herb2 not in lowland.fauna_dict["Herbivore"]
        #Carnivore eats both herbivores. Increase the weight so it only has to eat one

    def test_no_birth_when_mother_loses_more_than_her_weight(self, landscape_data, mocker):
        mocker.patch("numpy.random.uniform", return_value=0)
        lowland = landscape_data['L']
        self.herb1 = lowland.fauna_dict['Herbivore'][0]
        self.herb2 = lowland.fauna_dict['Herbivore'][1]
        pass
        ##wait

    def test_weight_after_breeding_is_decreased(self):
        pass









    class TestWater:
        @pytest.fixture
        def water(self):
            return Water()

        def test_initiate_water(self, water):
            assert water

        def test_water_not_migratable(self, water):
            assert water.is_migratable is False

        def test_water_food_available(self, water):
            with pytest.raises(ValueError):
                water.remaining_food()

    class TestDesert:
        @pytest.fixture
        def desert(self):
            return Desert()

        def test_initiate_desert(self, desert):
            assert desert

        def test_desert_is_migratable(self, desert):
            assert desert.is_migratable is True

        def test_desert_food_available(self, desert):
            assert desert.remaining_food['Herbivore'] == 0
            assert desert.remaining_food['Carnivore'] == desert.total_herbivore_weight

    class TestHighland:
        @pytest.fixture
        def highland(self):
            return Highland()

        def test_initiate_highland(self, highland):
            assert highland

        def test_highland_is_migratable(self, highland):
            assert highland.is_migratable is True

        def test_highland_food_available(self, highland):
            assert highland.remaining_food['Herbivore'] == 300
            assert highland.remaining_food['Carnivore'] == highland.total_herbivore_weight

    class TestLowland:
        @pytest.fixture
        def lowland(self):
            return Lowland()

        def test_initiate_lowland(self, lowland):
            assert lowland

        def test_lowland_is_migratable(self, lowland):
            assert lowland.is_migratable is True

        def test_lowland_food_available(self, lowland):
            assert lowland.remaining_food['Herbivore'] == 800
            assert lowland.remaining_food['Carnivore'] == lowland.total_herbivore_weight