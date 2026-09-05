import pandas as pd

df = pd.read_csv("defects.csv")
df = df.dropna()
df = df.reset_index(drop=True)
df = df[df["status"] == "done"]
df = df.groupby("defect_type")["repair_cost"].sum()
print(df)
