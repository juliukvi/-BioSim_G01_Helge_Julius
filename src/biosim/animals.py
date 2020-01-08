# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'
import math as m
import random
import numpy as np
standard_parameters_herb = {
    "w_birth" : 8.0,
    "sigma_birth" : 1.5,
    "beta" : 0.9,
    "eta" : 0.05,
    "a_half" : 40.0,
    "phi_age" : 0.2,
    "w_half" : 10.0,
    "phi_weight" : 0.1,
    "mu" : 0.25,
    "lambda" : 1.0,
    "gamma" : 0.2,
    "zeta" : 3.5,
    "xi" : 1.2,
    "omega" : 0.4,
    "F" : 10.0,
}

standard_parameters_carn = {
    "w_birth" : 6.0,
    "sigma_birth" : 1.0,
    "beta" : 0.75,
    "eta" : 0.125,
    "a_half" : 60.0,
    "phi_age" : 0.4,
    "w_half" : 4.0,
    "phi_weight" : 0.4,
    "mu" : 0.4,
    "lambda" : 1.0,
    "gamma" : 0.8,
    "zeta" : 3.5,
    "xi" : 1.1,
    "omega" : 0.9,
    "F" : 50.0,
    "DeltaPhiMax" : 10.0
}

class Herb:
    def __init__(self, parameters):
        for key in parameters:
            setattr(self, key, parameters[key])
        self.fitness = 0
        self.w = np.random.normal(self.w_birth, self.sigma_birth)
        self.a = 0

    def age(self):
        self.a += 1

    def fitness(self):
        if self.weight <= 0:
            self.fitness = 0
        else:
            self.fitness = 1 / (1 + m.exp(
                self.phi_age * (self.a - self.a_half))) * 1 / (1 + m.exp(
                -self.phi_age(self.w - self.w_half)))


    def weight(self):

    def birth(self):
        prob = min(1, self.gamma * self.fitness * (self.num_herb - 1))
        number = random.random
        if len(island(self.pos).herb_list) < 2:
        prob = 0
        if self.weight < self.zeta * (w_birth + sigma_birth):
             prob = 0
        if number >= prob: