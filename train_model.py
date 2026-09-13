import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mentor@localhost:5432/railway")

sql_query = """
SELECT
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
    "Machine failure"
FROM ai4i2020
"""
df = pd.read_sql_query(sql_query, engine)
df["Power [W]"] = df["Rotational speed [rpm]"] * df["Torque [Nm]"] * 0.10472
df["Temperature gradient [K]"] = (
    df["Process temperature [K]"] - df["Air temperature [K]"]
)
df["Type"] = df["Type"].map({"L": 0, "M": 1, "H": 2})
df["Overstrain"] = df["Tool wear [min]"] * df["Torque [Nm]"]

X = df.drop(columns=["Machine failure"])
y = df["Machine failure"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = RandomForestClassifier(
    n_estimators=100, max_depth=10, random_state=42, class_weight="balanced"
)
model.fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
for t in np.arange(0.15, 0.33, 0.03):
    y_pred_custom = (proba >= t).astype(int)
    cm = confusion_matrix(y_test, y_pred_custom)
    print(f"Порог: {t:.2f} | FN (пропуски): {cm[1, 0]} | FP (ложные): {cm[0, 1]}")
accuracy = accuracy_score(y_test, y_pred_custom)
print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nОтчет по классификации:")
print(classification_report(y_test, y_pred_custom))

for name, importance in zip(X.columns, model.feature_importances_):
    print(f"{name}: {importance:.3f}")

artifact = {"model": model, "threshold": 0.15, "features": list(X.columns)}

joblib.dump(artifact, "predictive_maintenance_rf.joblib")
print("\nМодель и метаданные успешно сохранены в predictive_maintenance_rf.joblib")
