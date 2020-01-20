# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'
from biosim.animals import Carn, Herb
from biosim.landscape import Jungle, Savannah, Mountain, Ocean, Desert
import pytest


class TestBaseNature:
    @pytest.fixture
    def jungle(self):
        return Jungle()
    @pytest.fixture
    def savannah(self):
        return Savannah()
    @pytest.fixture
    def herb_list(self):
        return [Herb() for _ in range(100)]
    @pytest.fixture
    def carn_list(self):
        return [Carn() for _ in range(100)]

    def test_sorting_list_by_fitness_in_feed_all_animals(
            self, herb_list, carn_list):
        herb_list = herb_list
        carn_list = carn_list
        herb_list.sort(key=lambda x: x.fitness, reverse=True)
        carn_list.sort(key=lambda x: x.fitness, reverse=True)
        fit_list_herb = [h.fitness for h in herb_list]
        fit_list_carn = [c.fitness for c in carn_list]
        assert all([fit_1 > fit_2 for fit_1, fit_2 in
                    zip(fit_list_herb[:-1], fit_list_herb[1:])])
        assert all([fit_1 > fit_2 for fit_1, fit_2 in
                    zip(fit_list_carn[:-1], fit_list_carn[1:])])

    def test_aging_all_animals(self, jungle, herb_list, carn_list):
        j = jungle
        j.herb_list = herb_list
        j.carn_list = carn_list
        j.aging_all_animals()
        for animal in j.herb_list:
            assert animal.a == 1
        for animal in j.carn_list:
            assert animal.a == 1

    def test_birth_all_animals(self, mocker):
        mocker.patch('random.uniform', return_value=0)
        herb_list = [Herb() for _ in range(1000)]
        carn_list = [Carn() for _ in range(1000)]
        j = Jungle()
        j.herb_list = herb_list
        j.carn_list = carn_list
        for h in herb_list:
            h.fitness = 1
            h.weight = 100
        for c in carn_list:
            c.fitness = 1
            c.weight = 100
        herbs_before_birth = j.herb_list





#def test_weightloss_all_animals(self):

#def test_death_all_animals(self):


class TestOcean:
    @pytest.fixture
    def ocean(self):
        return Ocean()

    def test_initiate_ocean(self, ocean):
        assert ocean

    def test_ocean(self, ocean):
        assert ocean.habitable is False
        assert ocean.fodder == 0


class TestMountain:
    @pytest.fixture
    def mountain(self):
        return Mountain()

    def test_initiate_mountain(self, mountain):
        assert mountain

    def test_init_function_mountain(self, mountain):
        assert mountain.habitable is False
        assert mountain.fodder == 0


class TestDesert:
    @pytest.fixture
    def desert(self):
        return Desert()

    def test_initiate_desert(self, desert):
        assert desert

    def test_init_desert(self, desert):
        assert desert.habitable is True


class TestSavannah:
    @pytest.fixture
    def savannah(self):
        return Savannah()

    @pytest.fixture
    def savannah_params(self):
        return {"f_max": 400, "alpha": 0.4}

    @pytest.fixture
    def tear_down_params(self):
        yield None
        Savannah().set_default_parameters_for_savannah()

    def test_initiate_savannah(self, savannah):
        assert savannah

    def test_init_savannah(self, savannah):
        assert savannah.fodder == savannah.f_max
        assert savannah.habitable is True

    def test_set_parameters_savannah_raises_errors(self, savannah):
        dict_with_key_error = {"f_max": 400, "key_not_valid": 1}
        with pytest.raises(KeyError):
            savannah.set_parameters(dict_with_key_error)
        assert savannah.DEFAULT_PARAMETERS["f_max"] == 300
        with pytest.raises(ValueError):
            savannah.set_parameters({"f_max": [1, 2]})
        with pytest.raises(ValueError):
            savannah.set_parameters({"f_max": -1})
    def test_set_parameters_savannah(
            self, savannah, savannah_params, tear_down_params
    ):
        savannah.set_parameters(savannah_params)
        assert savannah.parameters["f_max"] == 400
        assert savannah.parameters["alpha"] == 0.4

    def test_set_default_parameters_savannah(self, savannah, savannah_params):
        savannah.set_default_parameters_for_savannah()
        assert savannah.parameters == savannah.DEFAULT_PARAMETERS
        savannah.set_parameters(savannah_params)
        savannah.set_default_parameters_for_savannah()
        assert savannah.parameters == savannah.DEFAULT_PARAMETERS

    def test_set_attributes_as_params_savannah(
            self, savannah, savannah_params, tear_down_params
    ):
        savannah.set_parameters(savannah_params)
        assert savannah.f_max == 400
        assert savannah.alpha == 0.4

    def test_set_default_params_as_attributes_savannah(self, savannah):
        savannah.set_default_parameters_for_savannah()
        assert savannah.f_max == 300
        assert savannah.alpha == 0.3

    def test_savannah_fodder_update(self, savannah):
        s = savannah
        s.fodder = 100
        s.fodder_update()
        assert s.fodder == 100 + s.alpha * (s.f_max - 100)


class TestJungle:
    @pytest.fixture
    def jungle(self):
        return Jungle()

    @pytest.fixture
    def jungle_params(self):
        return {"f_max": 900}

    @pytest.fixture
    def tear_down_params(self):
        yield None
        Jungle().set_default_parameters_for_jungle()

    def test_initiate_jungle(self, jungle):
        assert jungle

    def test_set_parameters_jungle_raises_errors(self, jungle, jungle_params):
        dict_with_key_not_valid = {"key_not_valid": 1}
        with pytest.raises(KeyError):
            jungle.set_parameters(dict_with_key_not_valid)
        assert jungle.parameters["f_max"] == 800
        jungle.set_parameters(jungle_params)
        assert jungle.parameters["f_max"] == 900
        with pytest.raises(ValueError):
            jungle.set_parameters({"f_max": {"this is a dictionary": 1}})
        with pytest.raises(ValueError):
            jungle.set_parameters({"f_max": -3})

    def test_set_default_parameters_jungle(
            self, jungle, jungle_params, tear_down_params
    ):
        jungle.set_default_parameters_for_jungle()
        assert jungle.parameters == jungle.DEFAULT_PARAMETERS
        jungle.set_parameters(jungle_params)
        jungle.set_default_parameters_for_jungle()
        assert jungle.parameters == jungle.DEFAULT_PARAMETERS

    def test_set_default_params_as_attributes_jungle(self, jungle):
        jungle.set_default_parameters_for_jungle()
        assert jungle.f_max == 800

    def test_set_params_as_attributes_jungle(
            self, jungle, jungle_params, tear_down_params):
        jungle.set_parameters(jungle_params)
        assert jungle.f_max == 900

    def test_init_jungle(self, jungle):
        assert jungle.habitable is True
        assert jungle.fodder == jungle.f_max

    def test_jungle_fodder_update(self, jungle):
        j = jungle
        j.fodder = 100
        j.fodder_update()
        assert j.fodder == j.f_max   
