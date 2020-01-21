# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal, Adam Julius Olof Kviman'
__email__ = 'hegkleme@nmbu.no, juliukvi@nmbu.no'
from biosim.animals import Herb, Carn
import pytest
import numpy as np
from scipy.stats import normaltest, binom_test
import math as m


class TestBaseAnimal:
    """A testclass for the BaseAnimal class in animals.
    """
    @pytest.fixture
    def herb(self):
        """Creates a fixture of the herbivore class instance.
        """
        return Herb()

    @pytest.fixture
    def carn(self):
        """Creates a fixture of the herbivore class instance.
        """
        return Carn()

    @pytest.fixture
    def herb_params(self):
        """Creates a fixture of the herbivore default parameters.
        """
        return Herb().DEFAULT_PARAMETERS

    @pytest.fixture
    def carn_params(self):
        """Creates a fixture of the carnivore default parameters.
        """
        return Carn().DEFAULT_PARAMETERS

    @pytest.fixture
    def carn_list(self):
        """Creates a fixture that returns a list with 100 carnivores.
        """
        return [Carn() for _ in range(100)]

    @pytest.fixture
    def herb_list(self):
        """Creates a fixture that returns list with 100 herbivores.
        """
        return [Herb() for _ in range(100)]

    @pytest.fixture
    def ex_params(self):
        """Creates a fixture that returns a dictionary with new parameters.
        """
        return {"zeta": 4, "F": 15.0}

    @pytest.fixture
    def tear_down_params(self):
        """Creates a tear_down fixture that resets the parameters.
        """
        yield None
        Herb().set_default_parameters_for_species()
        Carn().set_default_parameters_for_species()

    def test_set_parameters_raises_errors(self, herb, carn):
        """Tests that the set_parameters class method raises correct errors.
        """
        dict_with_invalid_key = {"zeta": 4, "key_not_valid": 1}
        with pytest.raises(KeyError):
            herb.set_parameters(dict_with_invalid_key)
        with pytest.raises(KeyError):
            carn.set_parameters(dict_with_invalid_key)
        dict_with_invalid_value = {"zeta": "some_string", "F": 4}
        with pytest.raises(ValueError):
            herb.set_parameters(dict_with_invalid_value)
        with pytest.raises(ValueError):
            carn.set_parameters(dict_with_invalid_value)
        with pytest.raises(ValueError):
            carn.set_parameters({"DeltaPhiMax": 0})
        with pytest.raises(ValueError):
            herb.set_parameters({"F": -1})
        with pytest.raises(ValueError):
            herb.set_parameters({"eta": 3})

    def test_set_parameters(self, herb, carn, ex_params, tear_down_params):
        """Testing that the set_parameters updates the parameters dictionary.

        """
        herb.set_parameters(ex_params)
        carn.set_parameters(ex_params)
        assert herb.parameters["zeta"] == 4
        assert herb.parameters["F"] == 15.0
        assert carn.parameters["zeta"] == 4
        assert carn.parameters["F"] == 15.0

    def test_set_default_params_as_attr(self, herb, carn, ex_params):
        """"Tests if the default parameters gets set as attributes.

        The _set_params_as_attributes class method is called in the
        set_parameters_default_parameters class method, and as a result it's
        only
        necessary to call set_default_parameters to test.
        """
        herb.set_default_parameters_for_species()
        carn.set_default_parameters_for_species()
        assert herb.zeta == 3.5
        assert herb.F == 10.0
        assert carn.zeta == 3.5
        assert carn.F == 50.0
        assert herb.xi == herb.DEFAULT_PARAMETERS["xi"]
        assert carn.zeta == carn.DEFAULT_PARAMETERS["zeta"]

    def test_set_new_params_as_attributes(
            self, herb, carn, ex_params, tear_down_params, herb_list, carn_list
    ):
        """Tests if the new parameters gets set as attributes.

        The _set_default_params_as_attributes class method is called in the
        set_parameters class method, and as a result it's only
        necessary to call set_default_parameters to test.
        """
        herb.set_parameters(ex_params)
        carn.set_parameters(ex_params)
        assert herb.F == 15.0
        assert herb.zeta == 4
        assert carn.zeta == 4
        assert herb.zeta == 4
        h_2 = herb
        c_2 = carn
        assert h_2.F == 15.0
        assert c_2.F == 15.0
        assert all(h.zeta for h in herb_list)
        assert all(c.F for c in carn_list)

    def test_set_default_parameters_for_species(
            self, herb, carn, herb_params, carn_params, herb_list, carn_list
    ):
        """Tests that the set_default_parameter method resets the parameters.
        """
        herb.set_default_parameters_for_species()
        carn.set_default_parameters_for_species()
        assert herb.parameters == herb_params, 'Parameters are not default'
        assert carn.parameters == carn_params, 'Parameters are not default'
        herb.set_parameters({"xi": 500})
        carn.set_parameters({"zeta": 100})
        herb.set_default_parameters_for_species()
        carn.set_default_parameters_for_species()
        assert all(h.xi for h in herb_list), 'Parameters are not reset'
        assert all(c.xi for c in carn_list), 'Parameters are not reset'

    def test_baseanimal_init_function_inherits_correctly_to_subclass(
            self, herb, carn
    ):
        """Tests that the attributes inherits correctly to the animal species.

        This test function also tests if the class raises errors if the animals
        are initiated with incorrect value ranges.
        """
        assert herb.a == 0
        assert carn.a == 0
        assert carn.weight > 0
        assert herb.weight > 0
        assert 0 <= herb.fitness <= 1, 'Fitness needs to be in interval [0,1]'
        assert 0 <= carn.fitness <= 1, 'Fitness needs to be in interval [0,1]'
        with pytest.raises(ValueError):
            Herb(age=-1)
        with pytest.raises(ValueError):
            Carn(age=-300)
        with pytest.raises(ValueError):
            Herb(weight=-1)
        with pytest.raises(ValueError):
            Carn(weight=-1)
        with pytest.raises(ValueError):
            Herb(age="hello")
        with pytest.raises(ValueError):
            Carn(weight='hi')
        with pytest.raises(ValueError):
            Herb(weight=[1, 2, 3])

    def test_weight_follows_normal_distribution(self):
        """A statistical test for the distribution of animal weights.

        The test determines whether it is probable that the drawn weights of
        the animals follows a normal distribution.
        The test uses  the normaltest from scipy, which is based on D.agostinos
        K^2 test. The nullhypothesis for the test is that the weight follows a
        normal distribution. If the assertion fails we reject the
        nullhypothesis on the given significance level, which is defined
        as alpha.
        """
        n_trials = 10000
        some_herb_list = [Herb() for _ in range(n_trials)]
        some_carn_list = [Carn() for _ in range(n_trials)]
        weight_data_herb = [h.weight for h in some_herb_list]
        weight_data_carn = [c.weight for c in some_carn_list]
        stat, p_value1 = normaltest(weight_data_herb)
        stat, p_value2 = normaltest(weight_data_carn)
        alpha = 0.001
        assert p_value1 > alpha, "Herbivore weight probably " \
                                 "doesn't follow a normal distribution"
        assert p_value2 > alpha, "Carnivore weight probably " \
                                 "doesn't follow a normal distribution"

    def test_age_function(self, herb, carn):
        """Tests that the age_animal method works properly.
        """
        h = herb
        c = carn
        h.age_animal()
        c.age_animal()
        assert h.a == 1
        assert c.a == 1
        for _ in range(10):
            h.age_animal()
            c.age_animal()
        assert h.a == 11
        assert c.a == 11

    def test_migrate(self, mocker):
        """Tests that the migrate method works properly.

        The mocker is used to give spesific values from random functions used
        in the module.
        """
        mocker.patch('random.uniform', return_value=0)
        h = Herb()
        c = Carn()
        assert h.migrate() is True
        assert c.migrate() is True
        mocker.patch('random.uniform', return_value=1)
        h = Herb()
        c = Carn()
        assert h.migrate() is False
        assert c.migrate() is False

    def test_will_birth(self, mocker):
        """Tests that the will_birth method works correctly.

        The weights of herbivores and carnivores are set as needed to have the
        correct return object from the will_birth method.
        The mocker is used to give spesific values from random functions used
        in the module.
        """
        h = Herb()
        c = Carn()
        h.weight = 0
        c.weight = 0
        return_object_herb = h.will_birth(10)
        return_object_carn = c.will_birth(10)
        assert return_object_herb is None
        assert return_object_carn is None
        mocker.patch('random.uniform', return_value=0)
        h = Herb()
        c = Carn()
        h.weight = 100
        c.weight = 100
        return_object_herb = h.will_birth(10000)
        return_object_carn = c.will_birth(10000)
        assert isinstance(return_object_herb, Herb)
        assert isinstance(return_object_carn, Carn)

    def test_fitness_update(self, mocker):
        """Tests that the fitness gets updated for given values of weight.

        The mocker is used to give spesific values from random functions used
        in the module.
        """
        h = Herb()
        c = Carn()
        h.weight = -3
        c.weight = -2
        h.fitness_update()
        c.fitness_update()
        assert h.fitness == 0
        assert c.fitness == 0
        mocker.patch('numpy.random.normal', return_value=0)
        h = Herb()
        c = Carn()
        h.fitness_update()
        c.fitness_update()
        assert h.fitness == 0
        assert c.fitness == 0
        mocker.patch('numpy.random.normal', return_value=1)
        h = Herb()
        c = Carn()
        h.fitness_update()
        c.fitness_update()
        assert h.fitness == pytest.approx(
            1 / (1 + m.exp(h.phi_age * (h.a - h.a_half)))
            * 1 / (1 + m.exp(-h.phi_weight * (1 - h.w_half))))
        assert c.fitness == pytest.approx(
            1 / (1 + m.exp(c.phi_age * (c.a - c.a_half)))
            * 1 / (1 + m.exp(-c.phi_weight * (1 - c.w_half))))

    def test_birth(self, herb, carn):
        """Tests that the birth method returns the correct class instance.
        """
        assert isinstance(herb.birth(), Herb)
        assert isinstance(carn.birth(), Carn)

    def test_weightloss(self, mocker):
        """Tests that the weight is updated according to the weightloss method.

        The mocker is used to give spesific values from random functions used
        in the module.
        """
        mocker.patch('numpy.random.normal', return_value=1)
        h = Herb()
        h.weightloss()
        assert h.weight == 1 - h.eta * 1
        h.weight = 100000
        c = Carn()
        c.weight = 100000
        weight_list_herb = []
        weight_list_carn = []
        for _ in range(100):
            weight_list_herb.append(h.weight)
            weight_list_carn.append(c.weight)
            h.weightloss()
            c.weightloss()
        assert all([weight1 > weight2 for weight1,
                    weight2 in zip(weight_list_herb[:-1],
                                   weight_list_herb[1:])]),\
            'The weight does not decrease in the list when weightloss is used'
        assert all([weight1 > weight2 for weight1,
                    weight2 in zip(weight_list_carn[:-1],
                                   weight_list_carn[1:])]),\
            'The weight does not decrease in the list when weightloss is used'


    def test_death(self, mocker):
        """Tests that the death method works correctly.
        The fitness of herbivores and carnivores are set as needed to have the
        correct return object from the death method.
        The mocker is used to give spesific values from random functions used
        in the module.
        """
        h = Herb()
        c = Carn()
        h.fitness = 0
        c.fitness = 0
        assert h.death() is True
        assert c.death() is True
        h = Herb()
        c = Carn()
        mocker.patch('random.uniform', return_value=1)
        assert h.death() is False
        assert c.death() is False
        h = Herb()
        c = Carn()
        mocker.patch('random.uniform', return_value=0)
        assert h.death() is True
        assert c.death() is True

    def test_binomial_distribution_for_death_method(self, herb, carn):
        """A statistical test for the death_method.

        The test determines whether it is probable that the death method
        follows a binomial distribution given a fixed probability of death.
        The test uses the binomial_test from scipy.
        The nullhypothesis for the test is that the probability of death
        follows a binomial distribution. If the assertion fails we reject the
        nullhypothesis on the given significance level,
        which we have defined as alpha.

        """
        p_death = 0.3
        n_trials = 10000
        death_list_herb = []
        death_list_carn = []

        # Fitness value and omega value creates a p_death = 0.3 in death method
        herb.set_parameters({"omega": 1})
        for _ in range(n_trials):
            h = herb
            c = carn
            c.fitness = 0.7
            h.fitness = 0.7
            if h.death() is True:
                death_list_herb.append(h)
                death_list_carn.append(c)
        number_of_deaths_herb = len(death_list_herb)
        number_of_deaths_carn = len(death_list_carn)
        p_value1 = binom_test(number_of_deaths_herb, n_trials, p_death)
        p_value2 = binom_test(number_of_deaths_carn, n_trials, p_death)
        alpha = 0.001
        assert p_value1 > alpha
        assert p_value2 > alpha


class TestHerb:
    """Test class for Herb class in animals.
    """
    @pytest.fixture
    def herb(self):
        """Creates a fixture of the herbivore class instance.
        """
        return Herb()

    def test_initiate_herb(self, herb):
        """Tests if the herb class can be initiated.
        """
        assert herb, 'Herbivore class cannot be initiated.'

    def test_feeding_herb(self, mocker):
        """Tests that the feeding of herbivores are done correctly.

        The mocker is used to give spesific values from random functions used
        in the module.
        """
        mocker.patch('numpy.random.normal', return_value=3)
        h = Herb()
        return_fodder = h.feeding(300)
        assert h.weight == 3 + h.beta * h.F
        assert return_fodder == h.F
        h = Herb()
        return_fodder = h.feeding(5)
        assert h.weight == 3 + h.beta * 5
        assert return_fodder == 5
        with pytest.raises(ValueError):
            h.feeding(-5)


class TestCarn:
    """Test class for Carn class in animals.
    """
    @pytest.fixture
    def carn(self):
        """Creates a fixture of the carnivore class instance.
        """
        return Carn()

    @pytest.fixture
    def herb(self):
        """Creates a fixture of the herbivore class instance.
        """
        return Herb()

    @pytest.fixture
    def herb_list(self):
        """Creates a fixture that returns list with 100 herbivores.
        """
        return [Herb() for _ in range(100)]

    def test_initiate_carn(self, carn):
        assert carn

    def test_carnivore_doesnt_feed_if_fitness_or_appetite_low(
            self, carn, herb_list):
        """Tests that the carnivore stops feeding for given conditions.
        """
        herb_list = herb_list
        herb_list.sort(key=lambda x: x.fitness, reverse=True)
        c = carn
        c.F = 0
        killed_herbs = len(c.feeding(herb_list))
        assert killed_herbs == 0
        c = carn
        c.fitness = 0
        killed_herbs = len(c.feeding(herb_list))
        assert killed_herbs == 0

    def test_carnivore_feeds_if_appetite_and_fitness_is_high(
            self, carn, herb_list):
        """Tests that the carnivore continues to eat for given conditions.
        """
        herb_list = herb_list
        herb_list.sort(key=lambda x: x.fitness, reverse=True)
        c = carn
        c.F = 500
        c.fitness = 1
        killed_herbs = len(c.feeding(herb_list))
        assert killed_herbs > 0

    def test_carnivore_continues_to_feed_if_it_has_appetite(self, mocker):
        """Tests that the carnivores continues to feed.

        Tests that the carnivore feeds until there are no more herbivores on
        the nature square, given that its appetite and fitness is high.
        Mocker is used to ensure that the carnivore eats for certain.
        """
        herb_list = [Herb() for _ in range(100)]
        herb_list.sort(key=lambda x: x.fitness, reverse=True)
        mocker.patch('random.uniform', return_value=0)
        c = Carn()
        c.F = 100000
        c.fitness = 0.5
        for herb in herb_list:
            herb.fitness = 0.1
        killed_herbs = len(c.feeding(herb_list))
        assert killed_herbs == len(herb_list)

    def test_carnivore_weight_and_fitness_updates_after_feeding(
            self, mocker):
        """Tests that the carnivore weight and fitness updates after feeding.

        Mocker is used to ensure that the carnivore eats.
        """
        a = Herb()
        mocker.patch("random.uniform", return_value=0)
        c = Carn()
        c.F = 10000
        c.fitness = 1
        herb_list = [a]
        herb_list.sort(key=lambda x: x.fitness, reverse=True)
        herb_weight_list = [h.weight for h in herb_list]
        carn_weight = c.weight + c.beta * herb_weight_list[0]
        c.feeding(herb_list)
        assert c.weight == pytest.approx(carn_weight)
        assert c.fitness == pytest.approx(
            1 / (1 + m.exp(c.phi_age * (c.a - c.a_half))) *
            1 / (1 + m.exp(-c.phi_age * (c.weight - c.w_half))))
        c = Carn()
        c.fitness = 1
        c.F = 0.001
        herb_list[0].weight = 5
        carn_weight = c.weight + c.beta * c.F
        c.feeding(herb_list)
        assert c.weight == pytest.approx(carn_weight), "Weight doesn't update"
