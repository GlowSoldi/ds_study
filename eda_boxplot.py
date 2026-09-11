import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mentor@localhost:5432/railway")

sql_query = """
SELECT
    "Type",
    "Torque [Nm]"
FROM ai4i2020
"""
df = pd.read_sql_query(sql_query, engine)
plt.figure(figsize=(8, 6))
sns.boxplot(x="Type", y="Torque [Nm]", data=df)
plt.title("Распределение крутящего момента по типу оборудования")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()
