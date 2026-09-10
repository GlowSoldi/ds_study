import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mentor@localhost:5432/railway")

sql_query = """
WITH broken_machines AS (
SELECT 
    "Type", 
    "Tool wear [min]"
FROM ai4i2020
WHERE "Machine failure" = 1
)
SELECT 
    "Type", 
    AVG("Tool wear [min]") 
    AS avg_tool_wear
FROM broken_machines
GROUP BY 1
ORDER BY 2 DESC
"""
df = pd.read_sql_query(sql_query, engine)
print(df)
