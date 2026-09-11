import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mentor@localhost:5432/railway")

sql_query = """
SELECT
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
    "Machine failure"
FROM ai4i2020
"""
df = pd.read_sql_query(sql_query, engine)
corr_matrix = df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Корреляционная матрица параметров оборудования")
plt.show()
