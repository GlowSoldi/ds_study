import pandas as pd

train_fleet = [
    {"id": "ЧС4Т-210", "route_type": "suburban", "mileage": 15000, "defects": 0},
    {"id": "ВЛ80с-104", "route_type": "freight", "mileage": None, "defects": 3},
    {"id": "ЭП1М-645", "route_type": "suburban", "mileage": 82000, "defects": None},
    {"id": "2ТЭ25КМ-012", "route_type": "freight", "mileage": 45000, "defects": 0},
    {"id": "ЭД9М-0134", "route_type": "suburban", "mileage": None, "defects": None},
]
df = pd.DataFrame(train_fleet)
df["defects"] = df["defects"].fillna(0)
df = df.dropna()
df = df.reset_index(drop=True)
print(df)
