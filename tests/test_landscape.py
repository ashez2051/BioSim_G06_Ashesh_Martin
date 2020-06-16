import pytest
import numpy

from biosim.landscape import Landscape, Lowland, Water, Highland, Desert
from biosim.fauna import Herbivore, Carnivore
import os


class TestLandscape:
    """
    Test class for the landscape
    """

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
        """
        Tests the add_animals function after adding an additional animal (herb3)
        """
        lowland = landscape_data["L"]
        assert len(lowland.fauna_dict['Herbivore']) == 2
        herb3 = Herbivore()
        lowland.add_animal(herb3)
        assert len(lowland.fauna_dict['Herbivore']) == 3

    def test_remove_animals(self, landscape_data):
        """
        Tests the remove_animal function by removing an animal from a population of two and see \n
        if it equals one \n
        """
        lowland = landscape_data["L"]
        assert len(lowland.fauna_dict['Herbivore']) == 2
        lowland.remove_animal(self.herb1)
        assert len(lowland.fauna_dict['Herbivore']) == 1

    def test_herbivore_eats_in_lowland(self, landscape_data):
        """
        Tests if the herbivore eats while being in the lowland and specifically if the weight \n
        of the herbivore increases after eating \n
        """
        lowland = landscape_data['L']
        self.herb1 = lowland.fauna_dict['Herbivore'][0]
        herb1_weight_before_eat = self.herb1.weight
        lowland.animal_eats()
        herb1_weight_after_eat = self.herb1.weight
        assert herb1_weight_after_eat > herb1_weight_before_eat

    def test_carnivore_eats_herbivore_in_lowland(self, landscape_data, mocker):
        """
        Tests if a carnivore eats a herbivore in the lowland by mocking the random.uniform \n
        function inside carnivore_eats. \n
        """
        mocker.patch("numpy.random.uniform", return_value=0)
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        self.carn1 = lowland.fauna_dict["Carnivore"][0]
        weight_before = self.carn1.weight
        lowland.carnivore_eats()
        assert self.carn1.weight > weight_before

    def test_place_carn_and_herb_in_cell(self, landscape_data):
        """
        Tests if it works to place two animals of each species in a lowland cell and then check \n
        that the animal count is equal to the amount of animals that was placed \n
        """
        lowland = landscape_data["L"]
        count = lowland.cell_fauna_count
        assert count['Herbivore'] == 2 and count["Carnivore"] == 2

    def test_herbivore_doesnt_eat_in_the_desert(self, landscape_data):
        """
        Tests that the herbivore doesnt eat in the desert, and more specifically that the weight \n
        is equal after running the animal_eats function. The function for decreasing weight \n
        with age has not been run here \n
        """
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
        Places carnivores in a cell without any food and check the weight remains the same after
        not running the update weight with age function
        """
        highland = landscape_data["H"]
        self.carn1 = highland.fauna_dict["Carnivore"][0]
        weight_before = self.carn1.weight
        highland.animal_eats()
        weight_after = self.carn1.weight
        assert weight_before == weight_after

    def test_resets_fodder_each_year(self, landscape_data):
        """
        Tests if the fodder in the lowland is being reset after a year passes and checks if the
        fodder is equal to 800 after resetting after 10 years
        """
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        for _ in range(10):
            lowland.animal_eats()
            lowland.update_fodder()
        assert lowland.food_left["Herbivore"] == 800

    def test_herb_count_reduces_when_herb_gets_eaten(self, landscape_data, mocker):
        """
        Adds two herbivores and two carnivores and check if the herbivores gets eaten
        """""
        mocker.patch("numpy.random.uniform", return_value=0)
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        self.herb2 = lowland.fauna_dict["Herbivore"][1]
        self.carn1 = lowland.fauna_dict["Carnivore"][0]
        self.carn2 = lowland.fauna_dict["Carnivore"][1]

        lowland.carnivore_eats()

        assert lowland.cell_fauna_count["Herbivore"] == 0

    def test_animal_count_increases_when_animal_is_born(self, landscape_data, mocker):
        mocker.patch("biosim.fauna.Fauna.proba_animal_birth", return_value=True)
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        self.herb2 = lowland.fauna_dict["Herbivore"][1]
        initial_count = lowland.cell_fauna_count["Herbivore"]

        lowland.animal_gives_birth()
        assert initial_count < lowland.cell_fauna_count["Herbivore"]

    def test_calculation_of_total_herbivore_weight(self, landscape_data):
        """
        Tests the calculate total herbivore weight function by comparing to the sum of two \n
        animals \n
        """
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        self.herb2 = lowland.fauna_dict["Herbivore"][1]
        assert lowland.total_herbivore_weight() == (self.herb1.weight + self.herb2.weight)

    def test_remaining_food_for_herbs_is_correctly_calculated(self, landscape_data):
        """
        There are two animals
        """
        highland = landscape_data["H"]
        highland.herbivore_eats()
        assert len(highland.fauna_dict['Herbivore']) == 2
        assert highland.food_left["Herbivore"] == 280

    def test_sort_by_fitness_herb(self, landscape_data):
        """
        Tests the sort by fitness function on herbivores \n
        """
        lowland = landscape_data['L']
        lowland.sort_by_fitness()
        self.herb1 = lowland.fauna_dict['Herbivore'][0]
        self.herb2 = lowland.fauna_dict['Herbivore'][1]
        assert self.herb1.animal_fitness < self.herb2.animal_fitness

    def test_sort_by_fitness_carn(self, landscape_data):
        """
        Tests the sort by fitness function on carnivores \n
        """
        lowland = landscape_data['L']
        lowland.sort_by_fitness()
        self.carn1 = lowland.fauna_dict['Carnivore'][0]
        self.carn2 = lowland.fauna_dict['Carnivore'][1]
        assert self.carn1.animal_fitness > self.carn2.animal_fitness

    # def test_carnivore_eats_least_fit_herbivore(self, landscape_data, mocker):
    #     """
    #     Tests if a carnivore eats the least fit herbivore. Mocks the random.uniform function \n
    #     inside carnivore eats so it always eats the herbivores \n
    #     """
    #     mocker.patch("numpy.random.uniform", return_value=0)
    #     lowland = landscape_data['L']
    #     lowland.add_animal()
    #     assert herb1_fitness > herb2_fitness
    #     lowland.carnivore_eats()
    #     assert self.herb2 not in lowland.fauna_dict["Herbivore"]

    # def test_no_birth_when_mother_loses_more_than_her_weight(self, landscape_data, mocker):
    #     mocker.patch("numpy.random.uniform", return_value=0)
    #     lowland = landscape_data['L']
    #     self.herb1 = lowland.fauna_dict['Herbivore'][0]
    #     self.herb2 = lowland.fauna_dict['Herbivore'][1]
    #     pass  ##wait

    class TestWater:
        @pytest.fixture
        def water(self):
            return Water()

        def test_initiate_water(self, water):
            """
            Tests of the water object is being called \n
            """
            assert water

        def test_water_not_migratable(self, water):
            """
            Checks if water is migratable as it should not be \n
            """
            assert water.is_migratable is False


    class TestDesert:
        @pytest.fixture
        def desert(self):
            return Desert()

        def test_initiate_desert(self, desert):
            """
            Tests that the desert object is being called \n
            """
            assert desert

        def test_desert_is_migratable(self, desert):
            """
            Checks if the desert is migratable as it should be \n
            """
            assert desert.is_migratable is True

        def test_desert_food_available(self, desert):
            """
            Checks the available food in the desert. For herbivores this should be zero \n
            and for carnivores it should be the total herbivore weight \n
            """

            assert desert.food_left['Herbivore'] == 0
            assert desert.food_left['Carnivore'] == desert.total_herbivore_weight

    class TestHighland:
        @pytest.fixture
        def highland(self):
            return Highland()

        def test_initiate_highland(self, highland):
            """
            Tests that the highland object is being called \n
            """
            assert highland

        def test_highland_is_migratable(self, highland):
            """
            Checks if the highland is migratable as it should be \n
            """
            assert highland.is_migratable is True

        def test_highland_food_available(self, highland):
            """
            Checks the available food in the desert. For herbivores this should be 300 \n
            and for carnivores it should be the total herbivore weight \n
            """
            assert highland.food_left['Herbivore'] == 300
            assert highland.food_left['Carnivore'] == highland.total_herbivore_weight

    class TestLowland:
        @pytest.fixture
        def lowland(self):
            return Lowland()

        def test_initiate_lowland(self, lowland):
            """
            Tests if the lowland object is being called \n
            """
            assert lowland

        def test_lowland_is_migratable(self, lowland):
            """
            Tests if the lowland is migratable, which it should be \n
            """
            assert lowland.is_migratable is True

        def test_lowland_food_available(self, lowland):
            """
            Checks the available food in the desert. For herbivores this should be 800 \n
            and for carnivores it should be the total herbivore weight \n
            """
            assert lowland.food_left['Herbivore'] == 800
            assert lowland.food_left['Carnivore'] == lowland.total_herbivore_weight
