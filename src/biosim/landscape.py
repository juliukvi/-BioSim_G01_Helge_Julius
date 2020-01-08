# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'
standard_parameters_jung = {"f_max":800}
standard_parameters_sav = {"f_max":300, "alpha":0.3}

class Nature:
    def __init__(self):
        self.color = None
        self.fodder = 0
        self.habitable = True


class Ocean(Nature):
    def __init__(self):
        super().__init__()
        self.color = "Blue"
        self.habitable = False


class Mountain(Nature):
    def __init__(self):
        super().__init__()
        self.color = "Grey"
        self.habitable = False


class Desert(Nature):
    def __init__(self):
        super().__init__()
        self.color = "Brown"


class Savannah(Nature):
    def __init__(self, start_fodder):
        super().__init__()
        self.color = "White"
        self.fodder = start_fodder

    def fodder_update(self, max_fodder, alpha):
        self.fodder = self.fodder + alpha * (max_fodder - self.fodder)

    def eating_rules(self, f):
        if f <= self.fodder:
            self.fodder -= f
        elif (self.fodder > 0) and (self.fodder < f):
            self.fodder = 0


class Jungle(Nature):
    def __init__(self, start_fodder):
        super().__init__()
        self.color = "Green"
        self.fodder = start_fodder

    def fodder_update(self, max_fodder):
        self.fodder = max_fodder

    def eating_rules(self, f):
        if f <= self.fodder:
            self.fodder -= f
        elif (self.fodder > 0) and (self.fodder < f):
            self.fodder = 0
