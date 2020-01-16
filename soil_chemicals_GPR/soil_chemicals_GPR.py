import pandas as pd
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
import matplotlib.pyplot as plt

data = pd.read_excel('HW03.xlsx', sheet_name='Data')
sdata = data.sort_values(by='Fe2O3')
x = np.array(sdata['Fe2O3'])
y = np.array(sdata['Al2O3'])
kernel = 1.27*RBF(length_scale=1, length_scale_bounds=(2e-1,1))
X = np.atleast_2d(x).T
np.random.seed(1)
dy = 0.5 + 1.0*np.random.random(y.shape)
noise = np.random.normal(0,dy)
y += noise
gp = GaussianProcessRegressor(kernel=kernel, alpha=dy**2, n_restarts_optimizer=10)
gp.fit(X,y)
y_pred, sigma = gp.predict(X, return_std=True)
fig, ax = plt.subplots()
plt.errorbar(X.ravel(), y, dy, fmt='r.', markersize=10, label='Observations')
plt.plot(x, y_pred, 'b-', label='Prediction')
plt.fill(np.concatenate([x, x[::-1]]),
         np.concatenate([y_pred - 1.9600 * sigma, (y_pred + 1.9600 * sigma)[::-1]]),
         alpha=0.5, fc='b', ec='None', label='95% confidence interval')
plt.xlabel('$Fe2O3$')
plt.ylabel('$Al2O3$')
plt.legend(loc='upper left')
plt.show()