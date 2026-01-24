import pandas as pd
data={"Name": ["Nivi","Mili","Shinchan"],"Age": [20,21,5],"Marks": [85,90,88]}
df=pd.DataFrame(data)
print(df)
print(df.head())      
print(df.tail())        
print(df.shape)      
print(df.size)     
print(df.columns)     
print(df.index) 
print(df.info())        
print(df.describe())    
