import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mentor@localhost:5432/railway")

sql_query = """
SELECT 
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Machine failure"
FROM ai4i2020
"""
df = pd.read_sql_query(sql_query, engine)

sns.scatterplot(
    data=df,
    x="Rotational speed [rpm]",
    y="Torque [Nm]",
    hue="Machine failure",
    alpha=0.6,
)
plt.show()
