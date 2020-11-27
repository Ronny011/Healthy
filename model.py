import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import metrics  # for mean error calculations

data = pd.read_csv('Dataset.csv')
data = data[['Weight', 'Height']].drop_duplicates()


def mean_fill():
    filled = np.array([]).reshape(-1, 1)
    for i in range(Y.size):
        filled = np.concatenate((filled, avg), axis=0)
    print(filled)
    return filled


X = data.iloc[:, 1].values.reshape(-1, 1)  # values converts it into a numpy array
Y = data.iloc[:, 0].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
print(Y)
print(Y.shape)
print(Y.size)
avg = np.array(np.average(Y)).reshape(-1, 1)  # mean of y variable observations
print(avg)
# linreg = LinearRegression()  # create object for the class
# linreg.fit(X, Y)  # perform linear regression
# Y_pred = linreg.predict(X)  # make predictions
Y_pred = mean_fill()
print(Y_pred)

plt.scatter(X, Y, label='Observations')
plt.plot(X, Y_pred, color='red', label='Regression line - Mean')
# plt.xlabel('Height')
plt.ylabel('Weight')
plt.title('Simple linear regression')
plt.legend()
plt.show()
# print(linreg.predict(np.array([190]).reshape(1, -1)))


print('Mean Absolute Error:', metrics.mean_absolute_error(Y, Y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(Y, Y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(Y, Y_pred)))
