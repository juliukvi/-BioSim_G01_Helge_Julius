# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'
from biosim.animals import BaseAnimal, Herb, Carn
import pytest
import numpy as np
from scipy.stats import normaltest

def test_initiate_BaseAnimal():
    with pytest.raises(ValueError):
        BaseAnimal()

def test_init_function_Animal():
    a = Animal()
    assert a.fitness == 0


def test_initiate_herb():
    assert Herb()


def test_set_parameters_herb():
    h = Herb()
    with pytest.raises(KeyError):
        h.set_parameters({"key_not_valid": 1})
        h.set_parameters({"zeta":4, "key_not_valid":1})
    #checking that zeta variable has not been updated in standard_parameters.
    assert h.parameters["zeta"] == 3.5
    h.set_parameters({"zeta": 4, "F": 15.0})
    assert h.parameters["zeta"] ==4
    assert h.parameters["F"] == 15.0
    with pytest.raises(ValueError):
        h.set_parameters({"zeta": 3.5, "F": 'some string'})
    #Checking that zeta remains unchanged
    assert h.parameters["zeta"] == 4


def test_set_attributes_herb():
    H = Herb()
    assert H.are_params_set is True
    assert H.w_half == 10
    assert H.phi_weight == 0.1


def test_init_function():
    H = Herb()
    assert H.a == 0
    assert H.weight > 0
    assert 0 <= H.fitness <= 1, 'Fitness needs to be in the interval [0,1]'


def test_weight_probability_distribution():
    #should i seed here?
    #Should i use X^2 test?
    #Using D.agostinos K^2 test which is accessed from the normaltest in scipy
    n_trials = 1000
    list_of_herbivores = []
    for _ in range(n_trials):
        list_of_herbivores.append(Herb())
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
    H= Herb()
    H.age()
    assert H.a == 1
    for _ in range(10):
        H.age()
    assert H.a == 11


def test_feeding():
    H = Herb()
    H.weight = 3
    return_fodder = H.feeding(300)
    #Checking that weight gets updated
    assert H.weight == 3 + H.beta*H.F
    #Checking that we have the correct return foddervalue
    assert return_fodder == H.F
    H.weight = 3
    return_fodder = H.feeding(5)
    assert H.weight == 3 +H.beta*5
    assert return_fodder == 5
    #Testing that negative fodder value gives error
    with pytest.raises(ValueError):
        H.feeding(-5)


def test_fitness_update(mocker):
    # Getting wrong return value from mocker patch?
    mocker.patch('numpy.random.normal', return_value=0)
    h = Herb()
    h.fitness_update()
    assert h.fitness == 0
    #H.weight = 1
    mocker.patch('numpy.random.normal', return_value=1)
    h = Herb()
    h.fitness_update()
    assert h.fitness == pytest.approx(1 / (1 + m.exp(0.2 * (0 - 40))) * 1 / (1 + m.exp(-0.2*(1 - 10))))


def test_will_birth(mocker):
    mocker.patch('numpy.random.normal', return_value=1)
    H = Herb()
    return_value = H.will_birth(10)
    assert return_value is False
    H = Herb()
    H.weight = H.zeta * (H.w_birth + H.sigma_birth)
    # Testing for probability = 1
    return_value = H.will_birth(10000)
    assert return_value is True


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
