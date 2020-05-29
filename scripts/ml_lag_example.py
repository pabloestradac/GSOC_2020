# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 14:37:15 2020

@author: pablo
"""

# First import libpysal to load the spatial analysis tools.
import numpy as np
import libpysal
from spreg import ML_Lag

db = libpysal.io.open(libpysal.examples.get_path("baltim.dbf"),'r')
ds_name = "baltim.dbf"
y_name = "PRICE"
y = np.array(db.by_col(y_name)).T
y = y[:, np.newaxis]
x_names = ["NROOM","NBATH","PATIO","FIREPL","AC","GAR","AGE","LOTSZ","SQFT"]
x = np.array([db.by_col(var) for var in x_names]).T
ww = libpysal.io.open(libpysal.examples.get_path("baltim_q.gal"))
w = ww.read()
ww.close()
w_name = "baltim_q.gal"
w.transform = 'r'

# The specification of the model to be estimated can be provided as lists.
# Each equation should be listed separately. In this example, equation 1
# has HR80 as dependent variable and PS80 and UE80 as exogenous regressors.
# For equation 2, HR90 is the dependent variable, and PS90 and UE90 the
# exogenous regressors.

mllag = ML_Lag(y,x,w,name_y=y_name,name_x=x_names,
               name_w=w_name,name_ds=ds_name)

# The SUR method requires data to be provided as dictionaries. PySAL
# provides the tool sur_dictxy to create these dictionaries from the
# list of variables. The line below will create four dictionaries
# containing respectively the dependent variables (bigy), the regressors
# (bigX), the dependent variables' names (bigyvars) and regressors' names
# (bigXvars). All these will be created from the database (db) and lists
# of variables (y_var and x_var) created above.

# bigy,bigX,bigyvars,bigXvars = sur_dictxy(db,y_var,x_var)

# We can now run the regression and then have a summary of the output.

np.around(mllag.betas, decimals=4)
