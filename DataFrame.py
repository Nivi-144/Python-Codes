import pandas as pd
data={
    "Name":["Mili","Nivi","Mini","Sakshi"],
    "Age":[19,20,21,22],
    "Marks":[78,98,80,90]
}
df=pd.DataFrame(data)
print("Data Frame:")
print(df)
print("\n Firts two rows:")
print(df.head(2))
print("Column Names")
print(df["Name"])
print("\nStudents with marks more than 80")
print(df[df["Marks"]>80])