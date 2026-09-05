import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mentor@localhost:5432/railway")
df = pd.read_csv("defects.csv")
df.to_sql("defects", engine, if_exists="replace", index=False)
print("Таблица успешно загружена в базу данных!")
