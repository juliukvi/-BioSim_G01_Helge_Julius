# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'

import textwrap

def create_map(geogr):
    map_list = []
    map_dict = {"O": Ocean(), "S": Savannah(), "M": Mountain(), "J": Jungle(), "D": Desert()}
    geogr = textwrap.dedent(geogr)
    for line in geogr.splitlines():
        placeholder_list = []
        for j in line:
            try:
                placeholder_list.append(map_dict[j])
            except KeyError:
                raise ValueError
        map_list.append(placeholder_list)

    for i in map_list[0]:
        if not i.color == "blue":
            raise ValueError
    for i in map_list[len(map_list)-1]:
        if not i.color == "blue":
            raise ValueError
    for i in range(len(map_list)):
        if not map_list[i][0].color == "blue":
            raise ValueError
    for i in range(len(map_list)):
        if not map_list[i][len(map_list[0])-1].color == "blue":
            raise ValueError
    return map_list


standard_parameters_jung = {"f_max" : 800}
standard_parameters_sav = {"f_max" : 300, "alpha" : 0.3}
parameters_jung = dict(standard_parameters_jung)#creating copies
parameters_sav = dict(standard_parameters_sav)

class Nature:
    def __init__(self):
        self.color = None
        self.fodder = 0
        self.habitable = True
        self.herb_list = []
        self.carn_list = []

class Ocean(Nature):
    def __init__(self):
        super().__init__()
        self.habitable = False


class Mountain(Nature):
    def __init__(self):
        super().__init__()
        self.habitable = False


class Desert(Nature):
    def __init__(self):
        super().__init__()


class Savannah(Nature):
    standard_parameters = {"f_max": 300, "alpha": 0.3}

    @classmethod
    def set_parameters(cls, new_params):
        for key in new_params:
            if key not in cls.standard_parameters.keys():
                raise KeyError(f'Parameter {key} is not in valid')
            cls.standard_parameters.update(new_params)

    def __init__(self):
        super().__init__()
        for key in self.standard_parameters.keys():
            setattr(self, key, self.standard_parameters[key])
        self.fodder = self.f_max
    def fodder_update(self):
        self.fodder = self.fodder + self.alpha * (self.f_max - self.fodder)

    def eating_rules(self, f):
        if f <= self.fodder:
            self.fodder -= f
        elif (self.fodder > 0) and (self.fodder < f):
            self.fodder = 0


class Jungle(Nature):
    standard_parameters = {"f_max": 800}


    @classmethod
    def set_parameters(cls, new_params):
        for key in new_params:
            if key not in cls.standard_parameters.keys():
                raise KeyError(f'Parameter {key} is not in valid')
        cls.standard_parameters.update(new_params)

    def __init__(self):
        for key in self.standard_parameters:
            setattr(self, key, self.standard_parameters[key])
        super().__init__()
        self.fodder = self.f_max

    def fodder_update(self, max_fodder):
        self.fodder = self.f_max

    def eating_rules(self, f):
        if f <= self.fodder:
            self.fodder -= f
        elif (self.fodder > 0) and (self.fodder < f):
            self.fodder = 0