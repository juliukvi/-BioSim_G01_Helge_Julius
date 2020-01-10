# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal, Adam Julius Olof Kviman'
__email__ = 'hegkleme@nmbu.no, juliukvi@nmbu.no'
import math as m
import random
import numpy as np

standard_parameters_carn = {
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


class Herb:
    standard_parameters = {
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
    are_params_set = False

    @classmethod
    def set_parameters(cls, new_params):
        for key in new_params:
            if key not in cls.standard_parameters.keys():
                raise KeyError(f'Parameter {key} is not in valid')
        cls.standard_parameters.update(new_params)
        cls._set_params_as_attributes()

    @classmethod
    def _set_params_as_attributes(cls):
        for key in cls.standard_parameters:
            setattr(cls, key, cls.standard_parameters[key])
        cls.are_params_set = True

    def __init__(self):
        if not self.are_params_set:
            self._set_params_as_attributes()
        self.weight = np.random.normal(self.w_birth, self.sigma_birth)
        self.a = 0
        self.fitness = 0
        self.fitness_update()

    def age(self):
        self.a += 1

    def feeding(self, fodder):
        if fodder > self.F:
            self.weight += self.beta * self.F
            return self.F
        elif (fodder > 0) and (fodder < self.F):
            self.weight += self.beta * fodder
            return fodder
        if fodder < 0:
            raise ValueError("Cannot have negative foddervalue")
    def fitness_update(self):
        if self.weight <= 0:
            self.fitness = 0
        else:
            self.fitness = 1 / (1 + m.exp(self.phi_age * (self.a - self.a_half)))* 1 / (1 + m.exp(-self.phi_age*(self.weight - self.w_half)))
    def will_birth(self, num_herb):
        prob = min(1, self.gamma * self.fitness * (num_herb - 1))
        number = random.uniform(0, 1)
        if self.weight < self.zeta * (self.w_birth + self.sigma_birth):
            return False
        if number <= prob:
            return True
        else:
            return False

    def birth(self):
        return Herb()

    def weightloss(self):
        self.weight -= self.eta*self.weight

    def death(self):
        if self.fitness == 0:
            return True
        prob = self.omega * (1 - self.fitness)
        number = random.uniform(0, 1)
        if number <= prob:
            return True
        else:
            return False
