# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:16:21 2020

@author: pablo
"""

# First import libpysal to load the spatial analysis tools.
import libpysal
from libpysal.examples import load_example
from libpysal.weights import Queen
import spreg
# from spreg import GM_KKP
import numpy as np


# Open data on NCOVR US County Homicides (3085 areas).
nat = load_example('Natregimes')
db = libpysal.io.open(nat.get_path('natregimes.dbf'),'r')
nat_shp = libpysal.examples.get_path("natregimes.shp")
w = Queen.from_shapefile(nat_shp)
w.transform = 'r'

# Extract the HR (homicide rates) data in the 70's, 80's and 90's from the 
# DBF file and make it the dependent variable for the regression.
# Extract RD and PS in the same time periods from the DBF to be used as
# independent variables in the regression.

name_y = ['HR70','HR80','HR90']
y = np.array([db.by_col(name) for name in name_y]).T

name_x = ['RD70','RD80','RD90','PS70','PS80','PS90']
x = np.array([db.by_col(name) for name in name_x]).T

    
    