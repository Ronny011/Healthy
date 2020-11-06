import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# we will pull our dataframe from a file
# if a file doesn't exist, we will use the dataset script
df = pd.read_csv('Dataset.csv')
# pd.plotting.scatter_matrix(df, alpha=0.2)
# plt.show()

sns.set_theme(style="ticks")

# df = sns.load_dataset("penguins")
# sns.pairplot(df[['Inc', 'HR', 'time', 'Activity', 'Weight', 'Height', 'Age']])
# sns.pairplot(df[['Weight', 'Height']])
# plt.show()
# df.describe()
print(df[['Weight', 'Height']].corr(method='pearson'))
