import pandas as pd

data = pd.read_csv("./output.csv")
print(data)
x = data.iloc[0,8]
y = data.iloc[0,9]
print(x, y)
