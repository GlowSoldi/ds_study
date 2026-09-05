import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mentor@localhost:5432/railway")

sql_query = """
SELECT
    "Machine failure",
    AVG("Tool wear [min]") AS avg_wear
FROM ai4i2020
GROUP BY "Machine failure"
"""
prediction_df = pd.read_sql_query(sql_query, engine)
print(prediction_df)
