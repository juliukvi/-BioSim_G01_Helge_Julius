# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'
from biosim.animals import BaseAnimal, Herb, Carn
import pytest
import numpy as np
from scipy.stats import normaltest
import math as m


def test_initiate_BaseAnimal_gives_error():
    with pytest.raises(ValueError):
        BaseAnimal()

def test_initiate_herb():
    assert Herb()


def test_initiate_carn():
    assert Carn()


def test_birth_method():
    h = Herb()
    c = Carn()
    birth_herb = h.birth()
    birth_carn = c.birth()
    assert isinstance(birth_herb, Herb)
    assert isinstance(birth_carn, Carn)


def test_set_default_parameters_for_species():
    h = Herb()
    c = Carn()
    h.set_default_parameters_for_species()
    c.set_default_parameters_for_species()
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


def test_set_params_as_attributes():
    h = Herb()
    c = Carn()
    assert h.are_params_set is True
    assert c.are_params_set is True
    assert h.w_birth == 8.0
    assert c.w_birth == 6.0
    h.set_parameters({'w_birth': 5.0})
    assert h.w_birth == 5.0
    #Checking that carnivore attributte stays unchanged
    assert c.w_birth == 6.0
    c.set_parameters({'w_birth': 2.0})
    h2 = Herb()
    c2 = Carn()
    assert h2.w_birth == 5.0
    assert c2.w_birth == 2.0
    list_of_herbs = [Herb() for _ in range(100)]
    list_of_carns = [Carn() for _ in range(100)]
    assert all(Herb.zeta for Herb in list_of_herbs)
    assert all(Carn.F for Carn in list_of_carns)


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
    stat, p = normaltest(weight_data)
    # Significance level 0.01.
    alpha = 0.01
    #Nullhypothesis is that the weight follows a normal distribution.
    #Weight follows a normal distribution if the test is passed.
    #If it doesnt pass, we reject H0 on a 0.01 significance level. This
    #means that it is more likely that the data doesnt follow a normal
    #distribution. If it passes it means that its probable that it follows
    # a normal distribution but we cant say for sure.
    assert p > alpha
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


def test_will_birth(mocker):
    mocker.patch('numpy.random.normal', return_value=0)
    h = Herb()
    c = Carn()
    return_object_herb = h.will_birth(10)
    return_object_carn = c.
    assert return_object is None
    h = Herb()
    mocker.patch('Numpy.random.normal', return_value=1000)
    return_object = h.will_birth(10000)
    assert isinstance(return_object, Herb)


def test_birth():
    h = Herb()
    assert isinstance(h.birth(), Herb)


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
    # Should i have a statistical test here? Dont know the distribution of the
    # probability function.
