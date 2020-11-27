import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# we will pull our dataframe from a file
# if a file doesn't exist, we will use the dataset script
df = pd.read_csv('Dataset.csv')
df['cID'] = df['ID'].astype('category')
# pd.plotting.scatter_matrix(df, alpha=0.2)

sns.set_theme(style="ticks")

# df = sns.load_dataset("penguins")
sns.pairplot(df[['HR', 'Inc', 'TOD', 'Activity', 'Weight', 'Height', 'Age']][df['Inc'] == 'Lying'], hue='Inc')
# sns.pairplot(df[['Weight', 'Height']])
plt.show()
# df.describe()
# print(df[['Weight', 'Height']].corr(method='pearson'))
