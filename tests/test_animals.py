# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'
from biosim.animals import BaseAnimal, Herb, Carn
import pytest
import numpy as np
from scipy.stats import normaltest, binom_test
import math as m

class TestAnimal:
    @pytest.fixture
    def herb(self):
        return Herb()

    @pytest.fixture
    def carn(self):
        return Carn()
    @pytest.fixture
    def herb_params(self):
        return Herb().DEFAULT_PARAMETERS
    @pytest.fixture
    def carn_params(self):
        return Carn().DEFAULT_PARAMETERS

    @pytest.fixture
    def ex_params(self):
        return {"zeta": 4, "F": 15.0}

    @pytest.fixture
    def clean_up_params(self):
        yield None
        Herb().set_default_parameters_for_species()
        Carn().set_default_parameters_for_species()

    def test_birth_method(self, herb, carn):
        birth_herb = herb.birth()
        birth_carn = carn.birth()
        assert isinstance(birth_herb, Herb)
        assert isinstance(birth_carn, Carn)

    def test_set_parameters_raises_error(self, herb, carn):
        with pytest.raises(KeyError):
            herb.set_parameters({"key_not_valid": 1})
        with pytest.raises(KeyError):
            carn.set_parameters({"key_not_valid": 1})
        dict_key_error = {"zeta": 4, "key_not_valid": 1}
        with pytest.raises(KeyError):
            herb.set_parameters(dict_key_error)
        with pytest.raises(KeyError):
            carn.set_parameters(dict_key_error)
        dict_value_error = {"zeta": "some_string", "F": 4}
        with pytest.raises(ValueError):
            herb.set_parameters(dict_value_error)
        with pytest.raises(ValueError):
            carn.set_parameters(dict_value_error)

    def test_set_parameters(self, herb, carn, ex_params, clean_up_params):
        herb.set_parameters(ex_params)
        carn.set_parameters(ex_params)
        assert herb.parameters["zeta"] == 4
        assert herb.parameters["F"] == 15.0
        assert carn.parameters["zeta"] == 4
        assert carn.parameters["F"] == 15.0
        clean_up_params
    def test_set_default_params_as_attr(self, herb, carn, ex_params):
        """"
            Tests if the parameters have been set as attributes by the
            set_params_as_attributtes method, which is called in the
            set_parameters method.
        """
        assert herb.zeta == 3.5
        assert herb.F == 10.0
        assert carn.zeta == 3.5
        assert carn.F == 50.0

    def test_set_new_params_as_attributes(self, herb, carn, ex_params,clean_up_params):
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
        list_of_herbs = [herb for _ in range(100)]
        list_of_carns = [carn for _ in range(100)]
        assert all(h.zeta for h in list_of_herbs)
        assert all(c.F for c in list_of_carns)
        clean_up_params
def test_initiate_herb():
    assert Herb()
class TestHerbivore:
    pass
class TestCarnivore:
    pass
def test_initiate_carn():
    assert Carn()





def test_set_parameters():
    h = Herb()
    c = Carn()
    with pytest.raises(KeyError):
        h.set_parameters({"key_not_valid": 1})
    with pytest.raises(KeyError):
        h.set_parameters({"zeta": 4, "key_not_valid": 1})
    with pytest.raises(KeyError):
        c.set_parameters({'key_not_valid': 1})
    with pytest.raises(KeyError):
        c.set_parameters({'zeta': 3,'key_not_valid':2})
    # checking that zeta variable has not been updated in standard_parameters.
    assert h.parameters["zeta"] == 3.5
    h.set_parameters({"zeta": 4, "F": 15.0})
    assert h.parameters["zeta"] == 4
    assert h.parameters["F"] == 15.0
    with pytest.raises(ValueError):
        h.set_parameters({"zeta": 3.5, "F": 'some string'})
    # Checking that zeta remains unchanged
    assert h.parameters["zeta"] == 4


def test_set_default_parameters_for_species():
    h = Herb()
    c = Carn()
    c.set_default_parameters_for_species()
    h.set_default_parameters_for_species()
    assert h.parameters == {
            "w_birth": 8.0,
            "sigma_birth": 1.5,
            "beta": 0.9,
            "eta": 0.05,
            "a_half": 40.0,
            "phi_age": 0.2,
            "w_half": 10.0,
            "phi_weight": 0.1,
            "mu": 0.25,
            "lambda": 1.0,
            "gamma": 0.2,
            "zeta": 3.5,
            "xi": 1.2,
            "omega": 0.4,
            "F": 10.0,
        }
    assert c.parameters == {
            "w_birth": 6.0,
            "sigma_birth": 1.0,
            "beta": 0.75,
            "eta": 0.125,
            "a_half": 60.0,
            "phi_age": 0.4,
            "w_half": 4.0,
            "phi_weight": 0.4,
            "mu": 0.4,
            "lambda": 1.0,
            "gamma": 0.8,
            "zeta": 3.5,
            "xi": 1.1,
            "omega": 0.9,
            "F": 50.0,
            "DeltaPhiMax": 10.0
        }
    h.set_parameters({"xi": 500})
    c.set_parameters({"zeta":100})
    h.set_default_parameters_for_species()
    c.set_default_parameters_for_species()
    assert h.xi == h.DEFAULT_PARAMETERS["xi"]
    assert c.zeta == c.DEFAULT_PARAMETERS["zeta"]
    herb_list = [Herb() for _ in range(100)]
    carn_list = [Carn() for _ in range(100)]
    assert all(Herb.xi for Herb in herb_list)
    assert all(Carn.xi for Carn in carn_list)


def test_BaseAnimal_init_function_inherits_correctly_to_subclass():
    h = Herb()
    c = Carn()
    assert h.a == 0
    assert c.a == 0
    assert c.weight > 0
    assert h.weight > 0
    assert 0 <= h.fitness <= 1, 'Fitness needs to be in the interval [0,1]'
    assert 0 <= c.fitness <= 1, 'Fitness needs to be in the interval [0,1]'
    with pytest.raises(ValueError):
        h = Herb(age=-1)
    with pytest.raises(ValueError):
        c = Carn(age=-300)
    with pytest.raises(ValueError):
        h = Herb(weight=-1)
    with pytest.raises(ValueError):
        c = Carn(weight=-1)
    with pytest.raises(ValueError):
        h = Herb(age="hello")
    with pytest.raises(ValueError):
        c = Carn(weight='hi')
    with pytest.raises(ValueError):
        h = Herb(weight=[1,2,3])


def test_weight_follows_normal_distribution():
    np.random.seed(123)# need this?
    #Using D.agostinos K^2 test which is accessed from the normaltest in scipy
    n_trials = 1000
    list_of_herbivores = [Herb() for _ in range(n_trials)]
    weight_data = [h.weight for h in list_of_herbivores]
    stat, p_value = normaltest(weight_data)
    # Significance level 0.01.
    alpha = 0.01
    #Nullhypothesis is that the weight follows a normal distribution.
    #Weight follows a normal distribution if the test is passed.
    #If it doesnt pass, we reject H0 on a 0.01 significance level. This
    #means that it is more likely that the data doesnt follow a normal
    #distribution. If it passes it means that its probable that it follows
    # a normal distribution but we cant say for sure.
    assert p_value > alpha
    #Checking if 95% of data lays within two standard deviations of the mean.
    assert np.mean(weight_data) < np.mean([h.w_birth + 2*h.sigma_birth for h in list_of_herbivores])


def test_age_function():
    h = Herb()
    c = Carn()
    h.age()
    c.age()
    assert h.a == 1
    assert c.a == 1
    for _ in range(10):
        h.age()
        c.age()
    assert h.a == 11
    assert c.a == 11



def test_fitness_update(mocker):
    h = Herb()
    h.weight = -3
    h.fitness_update()
    assert h.fitness == 0
    mocker.patch('numpy.random.normal', return_value=0)
    h = Herb()
    h.fitness_update()
    assert h.fitness == 0
    mocker.patch('numpy.random.normal', return_value=1)
    h = Herb()
    h.fitness_update()
    assert h.fitness == pytest.approx(1 / (1 + m.exp(0.2 * (0 - 40))) * 1 / (1 + m.exp(-0.2*(1 - 10))))

def test_migrate(mocker):
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


def test_will_birth(mocker):
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


def test_birth():
    h = Herb()
    c = Carn()
    assert isinstance(h.birth(), Herb)
    assert isinstance(c.birth(), Carn)


def test_weightloss(mocker):
    mocker.patch('numpy.random.normal', return_value=1)
    h = Herb()
    h.weightloss()
    assert h.weight == 1 - h.eta*1


def test_death(mocker):
    h = Herb()
    h.fitness = 0
    assert h.death() is True
    h = Herb()
    mocker.patch('random.uniform', return_value=1)
    assert h.death() is False
    h = Herb()
    mocker.patch('random.uniform', return_value=0)
    assert h.death() is True

def test_binomial_distribution_for_death_method():
    #Testing if the death follows a binomial distribution for given probability
    #for death. Using the scipy binomial test.
    #H0-følger binomial distributuin
    #Ha følger ikke
    p_death = 0.3
    n_trials = 10000
    death_list = []
    # Fitness value and omega value creates a p_death = 0.3 in death method.
    Herb().set_parameters({"omega": 1})
    for _ in range(n_trials):
        h = Herb()
        h.fitness = 0.7
        if h.death() is True:
            death_list.append(h.death)
    number_of_deaths = len(death_list)
    p_value = binom_test(number_of_deaths, n_trials, p_death)
    alpha = 0.01
    assert p_value > alpha


def test_sorting_list_by_fitness():
    herb_list = [Herb() for _ in range(100)]
    herb_list.sort(key=lambda x: x.fitness, reverse=True)
    fit_list = [h.fitness for h in herb_list]
    assert all([fit_1 > fit_2 for fit_1, fit_2 in zip(fit_list[:-1], fit_list[1:])])


def test_carnivore_doesnt_feed_if_fitness_or_appetite_low():
    some_herb_list = [Herb() for _ in range(100)]
    some_herb_list.sort(key=lambda x: x.fitness, reverse=True)
    c = Carn()
    c.F = 0
    killed_herbs = len(c.feeding(some_herb_list))
    assert killed_herbs == 0
    c = Carn()
    c.fitness = 0
    killed_herbs = len(c.feeding(some_herb_list))
    assert killed_herbs == 0
def test_carnivore_feeds_if_appetite_and_fitness_is_high():
    some_herb_list = [Herb() for _ in range(100)]
    some_herb_list.sort(key=lambda x: x.fitness, reverse=True)
    c = Carn()
    c.F = 500
    c.fitness = 1
    killed_herbs = len(c.feeding(some_herb_list))
    assert killed_herbs > 0

def test_carnivore_continues_to_feed_if_it_has_appetite(mocker):
    some_herb_list = [Herb() for _ in range(100)]
    some_herb_list.sort(key=lambda x: x.fitness, reverse=True)
    mocker.patch('random.uniform', return_value=0)
    c = Carn()
    c.F = 100000
    c.fitness = 0.5
    for herb in some_herb_list:
        herb.fitness = 0
    killed_herbs = len(c.feeding(some_herb_list))
    assert killed_herbs == len(some_herb_list)

def test_carnivore_weight_and_fitness_updates_after_feeding():
    some_herb_list = [Herb(), Herb()]
    some_herb_list.sort(key=lambda x: x.fitness, reverse=True)
    total_herb_weight = sum([h.weight for h in some_herb_list])
    c = Carn()
    c.F = 100000
    c.fitness = 1
    carn_weight = c.weight
    c.feeding(some_herb_list)
    assert carn_weight == carn_weight +c.beta *total_herb_weight
    assert c.fitness ==  pytest.approx(1 / (1 + m.exp(c.phi_age* (c.a - c.a_half))) * 1 / (1 + m.exp(-c.phi_age*(c.weight - c.w_half))))


def test_if_weight_updates_when_carnivore_feeds():
    c = Carn()
    some_herb_list = [Herb() for _ in range(100)]
    some_herb_list.sort(key=lambda x: x.fitness, reverse=True)


def test_binomial_distribution_feeding_carnivore():
    pass

def test_feeding_herb(mocker):
    mocker.patch('numpy.random.normal', return_value=3)
    h = Herb()
    return_fodder = h.feeding(300)
    assert h.weight == 3 + h.beta*h.F
    assert return_fodder == h.F
    h = Herb()
    return_fodder = h.feeding(5)
    assert h.weight == 3 +h.beta*5
    assert return_fodder == 5
    with pytest.raises(ValueError):
        h.feeding(-5)


def test_migration_distribution_with_chi_squared():
    pass