import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mentor@localhost:5432/railway")

sql_query = """
SELECT
    "Type",
    COUNT(*) AS incident_count
FROM ai4i2020
WHERE "Machine failure" = 1
GROUP BY "Type"
ORDER BY incident_count DESC 
"""
prediction_df = pd.read_sql_query(sql_query, engine)
print(prediction_df)
