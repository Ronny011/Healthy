import pandas as pd
from scipy import stats as st

idvar = 3
df = pd.read_csv('Dataset.csv')
setA = df['HR'][(df['Activity'] == 'sitting') & (df['ID'] == idvar)]
setB = df['HR'][(df['Activity'] == '7') & (df['ID'] == idvar)]
print(setA)
print(setB)
# assuming equal variance for both sets, equal_var = True by default
print(st.ttest_ind(setA, setB))
