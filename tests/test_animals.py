# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'
from biosim.animals import *
import pytest


def test_initiate_herb():
    assert Herb()


def test_set_parameters_herb():
    H = Herb()
    with pytest.raises(KeyError):
        H.set_parameters({"key_not_valid": 1})
    with pytest.raises(KeyError):
        H.set_parameters({"zeta":4, "key_not_valid":1})
    #checking that zeta variable has not been updated in standard_parameters.
    assert H.standard_parameters["zeta"] == 3.5
    H.set_parameters({"zeta": 4, "F":15.0})
    assert H.standard_parameters["zeta"] ==4
    assert H.standard_parameters["F"] == 15.0
def test_set_attributes_herb():
    H = Herb()
    assert H.are_params_set == True
    H.set_parameters({"w_half": 5})
    assert H.w_half == 5
    #Testing if other parameters stays unchanged.
    assert H.phi_weight == 0.1


def test_init_function():
    H = Herb()
    assert H.a == 0
    assert H.weight > 0
    assert H.fitness != 0
    assert H.fitness < 1

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
    a = H.feeding(300)
    #Checking that weight gets updated
    assert H.weight == 3 + H.beta*H.F
    #Checking that we have the correct return foddervalue
    assert a == H.F
    H.weight = 3
    a = H.feeding(5)
    assert H.weight == 3 +H.beta*5
    assert a == 5
    #Testing that negative fodder value gives error
    with pytest.raises(ValueError):
        H.feeding(-5)

def test_fitness_update():
    H = Herb()
    H.weight = -3
    H.fitness_update()
    assert H.fitness == 0
    H.weight = 1
    H.fitness_update()
    assert H.fitness == 1 / (1 + m.exp(0.2 * (0 - 40)))* 1 / (1 + m.exp(-0.2*(1 - 10)))

def test_birth():
    H = Herb()
    H.birth(10)






