# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'
from biosim.landscape import *
import pytest

#def test_nature():


#def test_feed_all_animals(self):

#def test_birth_all_animals(self):

#def test_aging_all_animals(self):

#def test_weightloss_all_animals(self):

#def test_death_all_animals(self):



def test_ocean():
    o = Ocean()
    assert o.habitable is False
    assert o.fodder == 0

def test_mountain():
    m = Mountain()
    assert m.habitable == False


def test_desert():
    d = Desert()
    assert d.habitable == True


def test_set_parameters_savannah():
    s = Savannah()
    with pytest.raises(KeyError):
        s.set_parameters({"key_not_valid": 1})
        s.set_parameters({"f_max": 400, "key_not_valid": 1})
    # Testing that f_max variable has not been updated in standard_parameters.
    assert s.standard_parameters["f_max"] == 300
    s.set_parameters({"f_max": 400, "alpha": 0.4})
    assert s.standard_parameters["f_max"] == 400
    assert s.standard_parameters["alpha"] == 0.4
    with pytest.raises(ValueError):
        s.set_parameters({"f_max": [1, 2]})

def test_set_attributes_savannah():
    s = Savannah()
    assert s.are_params_set is True
    s.set_parameters({'f_max': 300})
    assert s.f_max == 300
    assert s.alpha == 0.3


def test_savannah_init():
    s = Savannah()
    assert s.fodder == s.f_max
    assert s.habitable is True


def test_savannah_fodder_update():
    s = Savannah()
    s.fodder = 100
    s.fodder_update()
    assert s.fodder == 100 +s.alpha *(s.f_max-100)

def test_set_parameters_jungle():
    j = Jungle()
    with pytest.raises(KeyError):
        j.set_parameters({"key_not_valid": 1})
        j.set_parameters({"f_max": 400, "key_not_valid": 1})
    # Testing that f_max variable has not been updated in standard_parameters.
    assert j.standard_parameters["f_max"] == 800
    j.set_parameters({"f_max": 900})
    assert j.standard_parameters["f_max"] == 900
    with pytest.raises(ValueError):
        j.set_parameters({"f_max": {"some string":1}})


def test_set_attributes_jungle():
    j = Jungle()
    j.set_parameters({"f_max": 800})
    assert j.are_params_set is True
    assert j.f_max == 800


def test_jungle_init():
    j = Jungle()
    assert j.fodder == j.f_max
    assert j.habitable is True


def test_jungle_fodder_update():
    j = Jungle()
    j.fodder = 100
    j.fodder_update()
    assert j.fodder == j.f_max