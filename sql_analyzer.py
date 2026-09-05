import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mentor@localhost:5432/railway")

sql_query = """
SELECT 
    l.route_type,
    SUM (d.repair_cost) AS total_spent
FROM defects AS d
JOIN locomotives AS l ON d.train_id = l.id
WHERE d.status = 'done'
GROUP BY l.route_type
"""
budget_df = pd.read_sql_query(sql_query, engine)
print(budget_df)
