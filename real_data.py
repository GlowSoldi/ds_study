import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mentor@localhost:5432/railway")
df = pd.read_csv("ai4i2020.csv")
df.to_sql("ai4i2020", engine, if_exists="replace", index=False)
print("Таблица успешно загружена в базу данных!")
df.info()
