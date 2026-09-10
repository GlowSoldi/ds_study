import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mentor@localhost:5432/railway")

sql_query = """
WITH ranked_parts AS (
SELECT
    "Product ID",
    "Type",
    "Tool wear [min]",
    DENSE_RANK() OVER(
    PARTITION BY "Type"
    ORDER BY "Tool wear [min]" DESC
    ) AS wear_rank
FROM ai4i2020
)
SELECT
    "Product ID",
    "Type",
    "Tool wear [min]",
    wear_rank
FROM ranked_parts
WHERE wear_rank <= 3
ORDER BY "Type", wear_rank ASC
"""
df = pd.read_sql_query(sql_query, engine)
print(df)
