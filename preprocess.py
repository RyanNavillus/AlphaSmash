import pandas

df = pandas.read_csv("data.csv")

# Fix column names
names = {col: df.columns[i-1] for i, col in enumerate(df.columns) if i >= 3 and i <= 124 and i % 2 == 0}
df.rename(columns=names, inplace=True)
print(df.columns)

wins = df.iloc[:, 3:-12:2]
losses = df.iloc[:, 4:-12:2]

print(wins.head())
print(losses.head())
