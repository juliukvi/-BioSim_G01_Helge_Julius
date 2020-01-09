# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal, Adam Julius Olof Kviman'
__email__ = 'hegkleme@nmbu.no, juliukvi@nmbu.no'
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

parameters_herb = dict(standard_parameters_herb)
parameters_carn = dict(standard_parameters_carn)



class Herb:
    def __init__(self, parameters_herb, loc):
        for key in parameters_herb:
            setattr(self, key, parameters_herb[key])
        self.fitness = 0
        self.w = np.random.normal(self.w_birth, self.sigma_birth)
        self.a = 0
        self.loc = loc
        self.row = self.pos[0]
        self.col = self.pos[1]
        #self.pos_list = maplist[self.row][self.col].herb_list

    def age(self):
        self.a += 1

    def feeding(self):
        row = self.pos[0]
        col = self.pos[1]
        fodder = maplist[row][col].fodder
        if fodder > F:
            self.weight += self.beta * F
            return F
        elif (fodder > 0) and (fodder < f):
            self.weight += self.beta * fodder
            return fodder  # returnerer tallet den har spist som kan legges inn
            # i eating_rules for å fjerne fodder fra ruten i simulasjonen.

    def fitness(self):
        if self.weight <= 0:
            self.fitness = 0
        else:
            self.fitness = 1 / (1 + m.exp(
                self.phi_age * (self.a - self.a_half))) * 1 / (1 + m.exp(
                -self.phi_age(self.w - self.w_half)))

    def birth(self):
        prob = min(1, self.gamma * self.fitness * (self.num_herb - 1))
        number = random.random
        if len(self.pos_list) < 2:
            prob = 0
        if self.weight < self.zeta * (self.w_birth + self.sigma_birth):
             prob = 0
        if number >= prob:
            #create a class instance of herbivore at the same position.
            return True

     def death(self):
        if self.fitness == 0:
            #pos_list.pop(pos_list.index(self))
            return True
        prob = self.omega * (1 - self.fitness)
        number = random.random
        if number > prob:
            #pos_list.pop(pos_list.index(self))
            return True
        else:
            return False
