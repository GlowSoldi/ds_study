import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mentor@localhost:5432/railway")

sql_query = """
SELECT
    CASE
        WHEN "Tool wear [min]" > 130 THEN 'Red zone'
        ELSE 'Green zone'
    END AS wear_status,
    COUNT(*) AS parts_count
FROM ai4i2020
GROUP BY 1
"""
risk_assessment_df = pd.read_sql_query(sql_query, engine)
print(risk_assessment_df)
