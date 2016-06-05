import numpy as np
import pandas as pd
from sklearn.svm import SVR
import matplotlib.pyplot as plt

# read in data
dfrm = pd.read_csv('./resources/monthly_2011_2015.csv')
rawMatrix = dfrm.as_matrix()
dataMatrix2 = np.delete(rawMatrix, 0, 1)
dataMatrix = np.delete(dataMatrix2, 0, 1)
x = np.zeros((35, 24))
y = np.zeros(35)
for i in range(25, 60):
    x[i - 25, :] = dataMatrix[i - 25:i - 1, 0]
    y[i - 25] = dataMatrix[i, 0]

svr_rbf = SVR(kernel='linear', C=1e3)
y_rbf = svr_rbf.fit(x, y).predict(x)
plt.scatter(x[:, 0], y, c='k', label='data')
plt.hold('on')
plt.plot(x[:, 0], y_rbf, c='g', label='RBF model')
plt.xlabel('data')
plt.ylabel('target')
plt.title('Support Vector Regression')
plt.legend()
plt.show()
