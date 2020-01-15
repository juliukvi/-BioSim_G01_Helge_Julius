# -*- coding: utf-8 -*-

"""
"""

__author__ = "Helge Helø Klemetsdal & Adam Julius Olof Kviman"
__email__ = "hege.helo.klemetsdal@nmbu.no & "

from biosim.landscape import *
from biosim.animals import *
from biosim.animals import *
from biosim.island import *
import pandas as pd
import numpy as np
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import textwrap


# update these variables to point to your ffmpeg and convert binaries
_FFMPEG_BINARY = 'ffmpeg'
_CONVERT_BINARY = 'magick'


class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        random.seed(seed)
        island_map = textwrap.dedent(island_map)
        self.island = Island(island_map, ini_pop=ini_pop)
        self._year = 0
        self._img_ctr = 0
        self._ymax_animals = ymax_animals
        self._cmax_animals = cmax_animals
        self._img_base = img_base
        self._img_fmt = img_fmt
        # Set to true after graphics has been initialized
        self._graphics_init = False

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == "Herbivore":
            H = Herb()
            H.set_parameters(params)
        elif species == "Carnivore":
            C = Carn()
            C.set_parameters(params)
        else:
            raise ValueError(f'Got non existing species {species} ')
    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == "J":
            J = Jungle()
            J.set_parameters(params)
        else:
            S = Savannah()
            S.set_parameters(params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """
        plt.figure()
        start_year = self._year
        while self.year < start_year + num_years:
            if img_years == None:
                img_years = vis_years

            if self.year % vis_years == 0:
                plt.plot(range(2+self.year), range(2+self.year))
                #update graphics
                pass
            if self.year % img_years == 0:
                self._save_graphics()


            self.island.one_year()
            self._year += 1

    def add_population(self, population):
        self.island.add_population(population)


    @property
    def year(self):
        """Last year simulated."""
        return self._year


    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.island.count_animals()[2]

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        herbivore_count, carnivore_count = self.island.count_animals()[:2]
        num_animals_dict = {"Herbivore":herbivore_count, "Carnivore":carnivore_count}
        return num_animals_dict
    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""
        animal_count_list = self.island.animals_on_square()
        pd_data = pd.DataFrame(data=animal_count_list, columns=['Row', 'Col', 'Herbivore', 'Carnivore'])
        return pd_data
    def make_movie(self, movie_fmt="mp4"):
        """
        Creates MPEG4 movie from visualization images saved.
        .. :note:
            Requires ffmpeg
        The movie is stored as img_base + movie_fmt
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_CONVERT_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def _setup_graphics(self):
        if not self._graphics_init:
            self._fig = plt.figure()
        if not self._graphics_init:
            self._animal_lines = self._fig.add_subplot(1, 1, 1)
            if self._ymax_animals:
                self._animal_lines.set_ylim(0, self._ymax_animals)
            else:
                self.





        self._graphics_init = True
    def _save_graphics(self):
        """Saves graphics to file if file name given."""

        if self._img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1