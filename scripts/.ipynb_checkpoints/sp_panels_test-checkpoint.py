'''
Spatial random effects panel model based on: :cite:`KKP2007` 

'''

__author__ = "Luc Anselin anselin@uchicago.edu, Pedro Amaral pedroamaral@cedeplar.ufmg.br"

from scipy import sparse as SP
import numpy as np
import ols as OLS
from utils import optim_moments, RegressionPropsY, get_spFilter, spdot
# import user_output as USER
# import summary_output as SUMMARY
# import regimes as REGI

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

full_weights = False


def _moments_kkp(ws, u, i, trace_w2=None):
    '''
    Compute G and g matrices for the KKP model.
    ...

    Parameters
    ----------

    ws          : Sparse matrix
                  Spatial weights sparse matrix   

    u           : array
                  Residuals. nx1 array assumed to be aligned with w
    
    i		    : integer
                  0 if Q0, 1 if Q1
    trace_w2    : float
                  trace of WW. Computed in 1st step and saved for step 2.

    Returns
    -------

    moments     : list
                  List of two arrays corresponding to the matrices 'G' and
                  'g', respectively.
    trace_w2    : float
                  trace of WW. Computed in 1st step and saved for step 2.

    '''
    N = ws.shape[0]
    T = u.shape[0]//N
    if i == 0:
        Q = SP.kron(SP.identity(T) - np.ones((T,T))/T,SP.identity(N))
    else:
        Q = SP.kron(np.ones((T,T))/T,SP.identity(N))
    Tw = SP.kron(SP.identity(T),ws)
    ub = Tw.dot(u)
    ubb = Tw.dot(ub)
    Qu = Q.dot(u)
    Qub = Q.dot(ub)
    Qubb = Q.dot(ubb)
    G11 = float(2*np.dot(u.T,Qub))
    G12 = float(-np.dot(ub.T,Qub))
    G21 = float(2*np.dot(ubb.T,Qub))
    G22 = float(-np.dot(ubb.T,Qubb))
    G31 = float(np.dot(u.T,Qubb)+np.dot(ub.T,Qub))
    G32 = float(-np.dot(ub.T,Qubb))
    if trace_w2 == None:
        trace_w2 = (ws.power(2)).sum()
    G23 = ((T-1)**(1-i))*trace_w2
    if i == 0:
        G = np.array([[G11,G12,N*(T-1)**(1-i)],[G21,G22,G23],[G31,G32,0]])/(N*(T-1)**(1-i))
    else:
        G = np.array([[G11,G12,0,N*(T-1)**(1-i)],[G21,G22,0,G23],[G31,G32,0,0]])/(N*(T-1)**(1-i))
    g1 = float(np.dot(u.T,Qu))
    g2 = float(np.dot(ub.T,Qub))    
    g3 = float(np.dot(u.T,Qub))
    g = np.array([[g1,g2,g3]]).T / (N*(T-1)**(1-i))                            
    return [G, g],trace_w2


def _get_Tau(ws, trace_w2):
    '''
    Computes Tau as in :cite:`KKP2007`.
    ...
    
    Parameters
    ----------
    ws          : Sparse matrix
                  Spatial weights sparse matrix   
    trace_w2    : float
                  trace of WW. Computed in 1st step of _moments_kkp
    '''
    N = ws.shape[0]
    T12 = 2*trace_w2/N
    wtw = ws.T.dot(ws)
    T22 = wtw.power(2).sum()
    wtpw = ws.T + ws
    T23 = wtw.multiply(wtpw).sum()
    d_wwpwtw = ws.multiply(ws.T).sum(0)+wtw.diagonal()
    T33 = d_wwpwtw.sum()
    Tau = np.array([[2*N,T12,0],[T12,T22,T23],[0,T23,T33]])/N
    return Tau


def _get_panel_data(y, x, w, name_y, name_x):
    '''
    Performs some checks on the data structure and converts from wide to long if needed.
    ...
    
    Parameters
    ----------
    y          : array
                 n*tx1 or nxt array for dependent variable
    x          : array
                 Two dimensional array with n*t rows and k columns for
                 independent (exogenous) variable or n rows and k*t columns
                 (note, must not include a constant term)
    name_y       : string or list of strings
                   Name of dependent variable for use in output
    name_x       : list of strings
                   Names of independent variables for use in output
    '''

    if y.shape[0]/w.n != y.shape[0]//w.n:
            raise Exception("y must be ntx1 or nxt, and w must be an nxn PySAL W object.")
    N,T = y.shape[0],y.shape[1]
    k = x.shape[1] // T
    if x.shape[0] != N and x.shape[0] != N*T:
            raise Exception("X must have either n rows and k*t columns or n*t rows and k columns.")
    if x.shape[1] != k and x.shape[1] != k*T:
            raise Exception("X must have either n rows and k*t columns or n*t rows and k columns.")
    if y.shape[1] > 1:
        message = "Assuming time data is in wide format, i.e. y[0] refers to T0, y[1], refers to T1, etc." \
                "\n Similarly, assuming x[0:k] refers to independent variables for T0, x[k+1:2k] refers to T1, etc."
        print("Warning: "+ message)
        #warnings.warn(message)

        if y.shape[1] != T:
            raise Exception("y in wide format must have t columns and be compatible with x's k*t columns.")

        bigy = y.reshape((y.size,1),order="F")

        bigx = x[:,0:T].reshape((N*T,1),order='F')
        for i in range(1,k):
            bigx = np.hstack((bigx,x[:,T*i:T*(i+1)].reshape((N*T,1),order='F')))
    else:
        bigy, bigx = y, x
    
    if name_y:
        if not isinstance(name_y, str) and not isinstance(name_y, list):
            raise Exception("name_y must either be strings or a list of strings.")
        if len(name_y) > 1 and isinstance(name_y, list):
            name_y = ''.join([i for i in name_y[0] if not i.isdigit()])
        if len(name_y) == 1 and isinstance(name_y, list):
            name_y = name_y[0]
    if name_x:
        if len(name_x) != k*T and len(name_x) != k:
                raise Exception("Names of columns in X must have exactly either k or k*t elements.")
        if len(name_x) > k:
            name_bigx = []
            for i in range(k):
                name_bigx.append(''.join([j for j in name_x[i*T] if not j.isdigit()]))
            name_x = name_bigx
       
    return bigy, bigx, name_y, name_x

ols = OLS.BaseOLS(y=y, x=x)
x, y, n, k, xtx = ols.x, ols.y, ols.n, ols.k, ols.xtx
N = w.n
T = y.shape[0]//N
moments, trace_w2 = _moments_kkp(w.sparse, ols.u, 0)
lambda1, sig_v = optim_moments(moments, all_par=True)
Tw = SP.kron(SP.identity(T),w.sparse)
ub = Tw.dot(ols.u)
ulu = ols.u - lambda1*ub
Q1 = SP.kron(np.ones((T,T))/T,SP.identity(N))
sig_1 = float(np.dot(ulu.T,Q1.dot(ulu))/N)
#print('initial_lamb_sig:',lambda1,sig_v,sig_1)
#print('theta:', 1 - np.sqrt(sig_v)/ np.sqrt(sig_1))
Xi_a = SP.diags([(sig_v*sig_v)/(T-1),sig_1*sig_1])
if full_weights:
    Tau = _get_Tau(w.sparse,trace_w2)
else:
    Tau = SP.identity(3)        
Xi = SP.kron(Xi_a,Tau)
moments_b,_ = _moments_kkp(w.sparse, ols.u, 1,trace_w2)
G = np.vstack((np.hstack((moments[0],np.zeros((3,1)))),moments_b[0]))
moments6 = [G,np.vstack((moments[1],moments_b[1]))]
lambda2,sig_vb,sig_1b = optim_moments(moments6, vcX=Xi.toarray(), all_par=True, start=[lambda1,sig_v,sig_1])
# 2a. reg -->\hat{betas}
theta =  1 -  np.sqrt(sig_vb)/np.sqrt(sig_1b)
#print('theta:', theta)
gls_w = SP.identity(N*T) - theta*Q1

#With omega
xs = gls_w.dot(get_spFilter(w, lambda2, x))
ys = gls_w.dot(get_spFilter(w, lambda2, y))
ols_s = OLS.BaseOLS(y=ys, x=xs)
self.predy = spdot(self.x, ols_s.betas)
self.u = self.y - self.predy
self.vm = ols_s.vm #Check
self.betas = np.vstack((ols_s.betas, lambda2, sig_vb, sig_1b))
self.e_filtered = self.u - lambda2 * SP.kron(SP.identity(T),
    w.sparse).dot(self.u)
self.t, self.n = T, N
self._cache = {}

