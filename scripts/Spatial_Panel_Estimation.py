# -*- coding: utf-8 -*-
"""
Created on Fri May 29 08:30:54 2020

@author: pablo
"""

import numpy as np
import sys 
sys.path.append(r"C:\Users\pablo\OneDrive - Escuela Superior Politécnica del Litoral\2 MECE\Others\GSoC\scripts\spreg-1")
import spreg

# First import libpysal to load the spatial analysis tools.
import libpysal
from libpysal.examples import load_example
from libpysal.weights import Queen

# Open data on NCOVR US County Homicides (3085 areas).
nat = load_example('Natregimes')
db = libpysal.io.open(nat.get_path('natregimes.dbf'),'r')
nat_shp = libpysal.examples.get_path("natregimes.shp")
w = Queen.from_shapefile(nat_shp)
w.transform = 'r'

name_y = ['HR70','HR80','HR90']
y = np.array([db.by_col(name) for name in name_y]).T

name_x = ['RD70','RD80','RD90','PS70','PS80','PS90']
x = np.array([db.by_col(name) for name in name_x]).T

model = spreg.Panel_ML(y, x, w, method="lu", 
                       name_y=name_y, name_x=name_x, name_ds="Natregimes")

print(model.summary)