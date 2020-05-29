# -*- coding: utf-8 -*-
"""
Created on Mon May 11 15:58:31 2020

@author: pablo
"""

import numpy as np
import numpy.linalg as la
from scipy import sparse as sp
from scipy.sparse.linalg import splu as SuperLU
from utils import RegressionPropsY, RegressionPropsVM, inverse_prod
from sputils import spdot, spfill_diagonal, spinv, spbroadcast
import diagnostics as DIAG
import user_output as USER
import summary_output as SUMMARY
# from w_utils import symmetrize
import libpysal
from libpysal import weights
try:
    from scipy.optimize import minimize_scalar
    minimize_scalar_available = True
except ImportError:
    minimize_scalar_available = False
    
def lag_c_loglik(rho, n, e0, e1, W):
    # concentrated log-lik for lag model, no constants, brute force
    er = e0 - rho * e1
    sig2 = spdot(er.T, er) / n
    nlsig2 = (n / 2.0) * np.log(sig2)
    a = -rho * W
    spfill_diagonal(a, 1.0)
    jacob = np.log(np.linalg.det(a))
    # this is the negative of the concentrated log lik for minimization
    clik = nlsig2 - jacob
    return clik

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
method = "full"
epsilon = 0.0000001

n, k = x.shape
ylag = weights.lag_spatial(w, y)
# b0, b1, e0 and e1
xtx = spdot(x.T, x)
xtxi = la.inv(xtx)
xty = spdot(x.T, y)
xtyl = spdot(x.T, ylag)
b0 = spdot(xtxi, xty)
b1 = spdot(xtxi, xtyl)
e0 = y - spdot(x, b0)
e1 = ylag - spdot(x, b1)
methodML = method.upper()

W = w.full()[0]     # moved here
res = minimize_scalar(lag_c_loglik, 0.0, bounds=(-1.0, 1.0),
                      args=(n, e0, e1, W), method='bounded',
                      tol=epsilon)

rho = res.x[0][0]

# compute full log-likelihood, including constants
ln2pi = np.log(2.0 * np.pi)
llik = -res.fun - n / 2.0 * ln2pi - n / 2.0
logll = llik[0][0]

# b, residuals and predicted values

b = b0 - rho * b1
betas = np.vstack((b, rho))   # rho added as last coefficient
u = e0 - rho * e1
predy = y - u

xb = spdot(x, b)

predy_e = inverse_prod(
    w.sparse, xb, rho, inv_method="power_exp", threshold=epsilon)
e_pred = y - predy_e
sig2 = spdot(u.T, u) / n

# information matrix
# if w should be kept sparse, how can we do the following:
a = -rho * W
spfill_diagonal(a, 1.0)
ai = spinv(a)
wai = spdot(W, ai)
tr1 = wai.diagonal().sum() #same for sparse and dense

wai2 = spdot(wai, wai)
tr2 = wai2.diagonal().sum()

waiTwai = spdot(wai.T, wai)
tr3 = waiTwai.diagonal().sum()
### to here

wpredy = weights.lag_spatial(w, predy_e)
wpyTwpy = spdot(wpredy.T, wpredy)
xTwpy = spdot(x.T, wpredy)

# order of variables is beta, rho, sigma2

v1 = np.vstack(
    (xtx / sig2, xTwpy.T / sig2, np.zeros((1, k))))
v2 = np.vstack(
    (xTwpy / sig2, tr2 + tr3 + wpyTwpy / sig2, tr1 / sig2))
v3 = np.vstack(
    (np.zeros((k, 1)), tr1 / sig2, n / (2.0 * sig2 ** 2)))

v = np.hstack((v1, v2, v3))

vm1 = la.inv(v)  # vm1 includes variance for sigma2
vm = vm1[:-1, :-1]  # vm is for coefficients only
