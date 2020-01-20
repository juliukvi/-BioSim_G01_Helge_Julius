# -*- coding: utf-8 -*-

"""
"""

__author__ = "Helge Helø Klemetsdal & Adam Julius Olof Kviman"
__email__ = "hege.helo.klemetsdal@nmbu.no & "

from biosim.landscape import *
from biosim.animals import *
from biosim.animals import Herb, Carn
from biosim.island import *
import pandas as pd
import numpy as np
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import textwrap
from matplotlib.widgets import Button


# update these variables to point to your ffmpeg and convert binaries
_FFMPEG_BINARY = r'C:\Users\hej\Downloads\ffmpeg-20200115-0dc0837-win64-static\ffmpeg-20200115-0dc0837-win64-static\bin\ffmpeg.exe'
_CONVERT_BINARY = r'C:\Program Files\ImageMagick-7.0.9-Q16\magick.exe'


class BioSim:
    """Simulation class for the ecosystem on the island.

    Parameters
    ----------
    island_map: string
        Multi-line string specifying island geography.
    ini_pop: list
        List of dictionaries specifying initial population.
    seed: int
        Integer used as random number seed.
    ymax_animals: float?
        Number specifying y-axis limit for graph showing animal numbers.
    cmax_animals: dict
        Dict specifying color-code limits for animal densities.
    img_base: string
        String with beginning of file name for figures, including path.
    img_fmt: string
        String with file type for figures, e.g. 'png'.

    Attributes
    ----------
    island_map : string
        Multi-line string specifying island geography with removed whitespace.
    island : Island
        Island class instance with island_map and ini_pop parameters as input.
    year : int
        The year the simulation is simulating.


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

        random.seed(seed)
        np.random.seed(seed)
        island_map = textwrap.dedent(island_map)
        self._island_map = island_map
        self._island = Island(island_map, ini_pop=ini_pop)
        self._year = 0
        self._img_ctr = 0
        self._ymax_animals = ymax_animals
        self._cmax_animals = cmax_animals
        self._img_base = img_base
        self._img_fmt = img_fmt
        self._img_pause_time = 1e-20
        # the following will be initialized by _setup_graphics
        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._animal_lines_ax = None
        self._herb_line = None
        self._carn_line = None
        self._animal_lines_ax_legend = None
        self._herb_map_ax = None
        self._herb_map = None
        self._carn_map_ax = None
        self._carn_map = None
        self._cmax_herb = None
        self._cmax_carn = None
        self._island_map_ax = None
        self._island_text_ax = None
        self._pause_ax = None
        self._pause_widget = None
        self._large_island = None

    def set_animal_parameters(self, species, params):
        """Sets parameters for animal species.

        Parameters
        ----------
        species : string
            Animal of a given species.
        params : dict
            New parameters to be set for the animal species.
        Raises
        ------
        ValueError:
            If the species does not exist.

        """
        if species == "Herbivore":
            h = Herb()
            h.set_parameters(params)
        elif species == "Carnivore":
            c = Carn()
            c.set_parameters(params)
        else:
            raise ValueError(f'Got non existing species {species} ')

    def set_landscape_parameters(self, landscape, params):
        """Sets parameters for landscape type.

        Parameters
        ----------
        landscape : string
            Landscape of a given type.
        params : dict
            New parameters to be set for given landscape.
        Raises
        ------
        ValueError
            If the given landscape type doesn't exist.

        """
        if landscape == "J":
            j = Jungle()
            j.set_parameters(params)
        elif landscape == "S":
            s = Savannah()
            s.set_parameters(params)
        else:
            raise ValueError(f'Only jungle and svannah landscapes can have parameters'
                             f' updated. Got landscape {landscape}')

    def simulate(self, num_years, vis_years=1, img_years=None):
        """Run simulation while visualizing the result.

        Parameters
        ----------
        num_years: int
            number of years to simulate
        vis_years: int
            years between visualization updates
        img_years: int
            years between visualizations saved to files (default: vis_years)
        Notes
        -----
            Image files will be numbered consecutively.
        """

        start_year = self._year
        self._final_year = start_year + num_years
        self._setup_graphics()
        self._update_graphics()
        plt.pause(self._img_pause_time)
        while self.year < self._final_year:
            self._island.one_year()
            self._year += 1
            if vis_years:
                if img_years is None:
                    img_years = vis_years
                if self.year % vis_years == 0:
                    self._update_graphics()
                if self.year % img_years == 0:
                    self._save_graphics()
                plt.pause(self._img_pause_time)

            while self._paused:
                plt.pause(0.05)

    def add_population(self, population):
        """Adds a population of animals to a given location on the island.

        Parameters
        ----------
        population : dict
            Dictionary with animals of given location and population.
        """
        self._island.add_population(population)

    @property
    def year(self):
        """Last year simulated.
        """
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island.
        """
        return self._island.count_animals()[2]

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary.
        """
        herbivore_count, carnivore_count = self._island.count_animals()[:2]
        num_animals_dict = {"Herbivore": herbivore_count, "Carnivore": carnivore_count}
        return num_animals_dict

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island.
        """
        animal_count_list = self._island.animals_on_square()
        pd_data = pd.DataFrame(data=animal_count_list, columns=['Row', 'Col', 'Herbivore', 'Carnivore'])
        return pd_data

    def make_movie(self, movie_fmt="mp4"):
        """Creates MPEG4 movie from visualization images saved.
        Notes
        -----
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
        """ Sets up the graphic window.
        """
        if self._fig is None:
            self._fig = plt.figure(figsize=(15, 9))
        if self._animal_lines_ax is None:
            self._animal_lines_ax = self._fig.add_axes([0.6, 0.6, 0.35, 0.35])
            self._animal_lines_ax.set_xlabel("Years")
            self._animal_lines_ax.set_ylabel("Animal count")
            if self._ymax_animals:
                self._animal_lines_ax.set_ylim(0, self._ymax_animals)
            else:
                self._animal_lines_ax.set_ylim(0, (self.num_animals+1)*1.3)
        # year axis limit on plot needs to updated when you run multiple
        # multiple simulations after each other
        self._animal_lines_ax.set_xlim(0, self._final_year+1)

        if (self._island.map_columns or self._island.map_rows) > 23:
            self._large_island = True

        if self._herb_line is None:
            # Creates plot object with no y-values that has the correct length,
            # y-data will be gathered and set by self._update_graphics
            herb_plot = self._animal_lines_ax.plot(np.arange(0, self._final_year+1),
                                                   np.full(self._final_year+1, np.nan),
                                                   label='Herbivores')
            # Saves the line object from herb_plot
            self._herb_line = herb_plot[0]
        else:
            # Collects the data of the current active herb_line
            xdata, ydata = self._herb_line.get_data()
            # Creates array of values for the new years that is about to be
            # simulated
            xnew = np.arange(xdata[-1] + 1, self._final_year+1)
            if len(xnew) > 0:  # Think this is unnecesary since _setup_graphics should not be called if self._final_year is equal to self._year
                ynew = np.full(xnew.shape, np.nan)
                self._herb_line.set_data(np.hstack((xdata, xnew)),
                                         np.hstack((ydata, ynew)))

        if self._carn_line is None:
            # Creates plot object with no y-values that has the correct length,
            # y-data will be gathered and set by self._update_graphics
            carn_plot = self._animal_lines_ax.plot(np.arange(0, self._final_year+1),
                                                   np.full(self._final_year+1, np.nan),
                                                   label='Carnivores')
            # Saves the line object from herb_plot
            self._carn_line = carn_plot[0]
        else:
            # Collects the data of the current active herb_line
            xdata, ydata = self._carn_line.get_data()
            # Creates array of values for the new years that is about to be
            # simulated
            xnew = np.arange(xdata[-1] + 1, self._final_year+1)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._carn_line.set_data(np.hstack((xdata, xnew)),
                                         np.hstack((ydata, ynew)))

        if self._animal_lines_ax_legend is None:
            self._animal_lines_ax.legend(loc="upper left")

        if self._cmax_animals is None:
            self._cmax_herb = 200
            self._cmax_carn = 50
        else:
            self._cmax_herb = self._cmax_animals["Herbivore"]
            self._cmax_carn = self._cmax_animals["Carnivore"]

        if self._herb_map_ax is None:
            self._herb_map_ax = self._fig.add_axes([0.05, 0.37, 0.25, 0.25])
            if self._large_island:
                self._herb_map_ax.set_xticks((0, self._island.map_columns-1))
                self._herb_map_ax.set_xticklabels((0, self._island.map_columns-1))
                self._herb_map_ax.set_yticks((0, self._island.map_rows-1))
                self._herb_map_ax.set_yticklabels((0, self._island.map_rows-1))
            else:
                self._herb_map_ax.set_xticks(range(self._island.map_columns))
                self._herb_map_ax.set_xticklabels(range(self._island.map_columns))
                self._herb_map_ax.set_yticks(range(self._island.map_rows))
                self._herb_map_ax.set_yticklabels(range(self._island.map_rows))
            self._herb_map_ax.set_title("Herbivore distribution")

        if self._carn_map_ax is None:
            self._carn_map_ax = self._fig.add_axes([0.05, 0.05, 0.25, 0.25])
            if self._large_island:
                self._carn_map_ax.set_xticks((0, self._island.map_columns-1))
                self._carn_map_ax.set_xticklabels((0, self._island.map_columns-1))
                self._carn_map_ax.set_yticks((0, self._island.map_rows-1))
                self._carn_map_ax.set_yticklabels((0, self._island.map_rows-1))
            else:
                self._carn_map_ax.set_xticks(range(self._island.map_columns ))
                self._carn_map_ax.set_xticklabels(range(self._island.map_columns))
                self._carn_map_ax.set_yticks(range(self._island.map_rows))
                self._carn_map_ax.set_yticklabels(range(self._island.map_rows))
                self._carn_map_ax.set_title("Carnivore distribution")

        if self._island_map_ax is None:
            rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                         'M': (0.5, 0.5, 0.5),  # grey
                         'J': (0.0, 0.6, 0.0),  # dark green
                         'S': (0.5, 1.0, 0.5),  # light green
                         'D': (1.0, 1.0, 0.5)}  # light yellow
            island_rgb = [[rgb_value[column] for column in row]
                        for row in self._island_map.splitlines()]
            island_rgb = np.array(island_rgb)
            self._island_map_ax = self._fig.add_axes([0.05, 0.7, 0.25, 0.25])  # llx, lly, w, h
            if self._large_island:
                self._island_map_ax.set_xticks((0, self._island.map_columns - 1))
                self._island_map_ax.set_xticklabels((0, self._island.map_columns - 1))
                self._island_map_ax.set_yticks((0, self._island.map_rows - 1))
                self._island_map_ax.set_yticklabels((0, self._island.map_rows - 1))
            else:
                self._island_map_ax.set_xticks(range(self._island.map_columns))
                self._island_map_ax.set_xticklabels(range(self._island.map_columns))
                self._island_map_ax.set_yticks(range(self._island.map_rows))
                self._island_map_ax.set_yticklabels(range(self._island.map_rows))
            self._island_map_ax.imshow(island_rgb)
            self._island_map_ax.set_title("Island map")
            map_rect = self._fig.add_axes([0.31, 0.7, 0.25, 0.25])  # llx, lly, w, h
            map_rect.axis('off')
            for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                                      'Savannah', 'Desert')):
               map_rect.add_patch(plt.Rectangle((0., ix * 0.2), 0.1, 0.1,
                                            edgecolor='none',
                                            facecolor=rgb_value[name[0]]))
               map_rect.text(0.12, ix * 0.2, name, transform=map_rect.transAxes)

        if self._island_text_ax is None:
            self._island_text_ax = self._fig.add_axes([0.48, 0.5, 0, 0])
            self._island_text_ax.axis('off')
            self._island_text_values = 'Year: {}     ' \
                                    'Total Animals: {}     ' \
                                    'Herbivores: {}     ' \
                                    'Carnivores: {}     '
            self._island_text = self._island_text_ax.text(0., 0.,
                                      self._island_text_values.format(
                                          self._year,
                                          self.num_animals,
                                          self.num_animals_per_species['Herbivore'],
                                          self.num_animals_per_species['Carnivore']),
                                      horizontalalignment='left',
                                      verticalalignment='top',
                                      transform=self._island_text_ax.transAxes,
                                      fontsize=14)

        if self._pause_ax is None:
            self._paused = False
            self._pause_ax = self._fig.add_axes([0.6, 0.10, 0.3, 0.15])
            self._pause_widget = Button(self._pause_ax, 'Pause/Run', hovercolor='0.5')
            self._pause_widget.on_clicked(self._pause_button_click)

    def _update_graphics(self):
        """Updates the figure with """
        self._update_animal_lines()
        self._update_animal_heat_maps()
        self._update_text()

    def _update_text(self):
        self._island_text.set_text(self._island_text_values.format(
            self.year,
            self.num_animals,
            self.num_animals_per_species['Herbivore'],
            self.num_animals_per_species['Carnivore']))

    def _pause_button_click(self, event):
        """ ?

        Parameters
        ----------
        event : ?

        Returns
        -------

        """
        if self._paused:
            self._paused = False
        else:
            self._paused = True

    def _update_animal_lines(self):
        """ Updates the animal lines in the graphics.
        """
        if self._ymax_animals is None:
            # Saves number of animals in a variable so that property num_animals dont need to be called multiple times
            number_of_animals = self.num_animals
            if number_of_animals > self._animal_lines_ax.get_ylim()[1]:
                self._animal_lines_ax.set_ylim(0, number_of_animals + 100)
        ydata_herb = self._herb_line.get_ydata()
        ydata_herb[self._year] = self.num_animals_per_species["Herbivore"]
        self._herb_line.set_ydata(ydata_herb)
        ydata_carn = self._carn_line.get_ydata()
        ydata_carn[self.year] = self.num_animals_per_species['Carnivore']
        self._carn_line.set_ydata(ydata_carn)

    def _update_animal_heat_maps(self):
        """Updates the animal heat maps in the graphics.
        """

        if self._herb_map is not None:
            self._herb_map.set_data(np.reshape(self.animal_distribution['Herbivore'].values,
                newshape=(self._island.map_rows, self._island.map_columns)))
        else:
            self._herb_map = self._herb_map_ax.imshow(np.reshape(self.animal_distribution[
                                                                     'Herbivore'].values,
                                                                 newshape=(self._island.map_rows,
                                                                           self._island.map_columns)),
                                                      vmax=self._cmax_herb)
            plt.colorbar(self._herb_map, ax=self._herb_map_ax,
                         orientation='vertical', fraction=0.05)

        if self._carn_map is not None:
            self._carn_map.set_data(np.reshape(self.animal_distribution['Carnivore'].values,
                                               newshape=(self._island.map_rows, self._island.map_columns)))
        else:
            self._carn_map = self._carn_map_ax.imshow(np.reshape(self.animal_distribution[
                                                                     'Carnivore'].values,
                                                                 newshape=(self._island.map_rows,
                                                                           self._island.map_columns)),
                                                      vmax=self._cmax_carn)
            plt.colorbar(self._carn_map, ax=self._carn_map_ax,
                         orientation='vertical', fraction=0.05)

    def _save_graphics(self):
        """Saves graphics to file if file name given.
        """

        if self._img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
