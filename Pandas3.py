import pandas as pd
s=pd.Series([10,20,30,40,50,None])
print(s)
print(s.isnull())
print(s.fillna(0))
print(s.dropna())

