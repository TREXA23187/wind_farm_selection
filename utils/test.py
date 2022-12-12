import numpy as np
import pysal.lib
import pysal
from pysal.model.spreg import diagnostics as D
from spreg.ml_lag import ML_Lag

db = pysal.lib.io.open(pysal.lib.examples.get_path("baltim.dbf"), 'r')

ds_name = 'baltim.dbf'
y_name = 'PRICE'


Y = np.array(db.by_col(y_name)).T
Y.shape = (len(Y), 1)

X_name = ['NROOM', 'NBATH', 'PATIO', 'FIREPL', 'AC', 'GAR', 'AGE', 'LOTSZ', 'SQFT']
X = np.array([db.by_col(var) for var in X_name]).T


ww = pysal.lib.io.open(pysal.lib.examples.get_path('baltim_q.gal'))
w = ww.read()
ww.close()

W_name = 'Baltim_q.gal'
w.transform = 'r'
ml_lag = ML_Lag(Y, X, w, name_y=y_name, name_x=X_name, name_w=W_name, name_ds=ds_name)

print(np.around(ml_lag.betas, decimals=4))
