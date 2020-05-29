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
from spreg import ML_Error_Regimes, sur_dictxy

# Open data on NCOVR US County Homicides (3085 areas).
nat = load_example('Natregimes')
db = libpysal.io.open(nat.get_path('natregimes.dbf'),'r')
nat_shp = libpysal.examples.get_path("natregimes.shp")
w = Queen.from_shapefile(nat_shp)
w.transform = 'r'

# The specification of the model to be estimated can be provided as lists. 
# Each equation should be listed separately. In this example, equation 1
# has HR80 as dependent variable and PS80 and UE80 as exogenous regressors.
# For equation 2, HR90 is the dependent variable, and PS90 and UE90 the
# exogenous regressors.

y_var = ['HR80','HR90']
x_var = [['PS80','UE80'],['PS90','UE90']]

# The SUR method requires data to be provided as dictionaries. PySAL
# provides the tool sur_dictxy to create these dictionaries from the
# list of variables. The line below will create four dictionaries
# containing respectively the dependent variables (bigy), the regressors
# (bigX), the dependent variables' names (bigyvars) and regressors' names
# (bigXvars). All these will be created from the database (db) and lists
# of variables (y_var and x_var) created above.

bigy,bigX,bigyvars,bigXvars = sur_dictxy(db,y_var,x_var)

# We can now run the regression and then have a summary of the output.

reg = spreg.SUR(bigy,bigX,w=w,
                name_bigy=bigyvars,name_bigX=bigXvars,
                spat_diag=True,name_ds="nat")
print(reg.summary)
    
    