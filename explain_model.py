import joblib
import matplotlib.pyplot as plt
import pandas as pd
import shap


def prepare_input(raw_data: dict, features_order: list[str]) -> pd.DataFrame:
    df = pd.DataFrame([raw_data])

    df["Power [W]"] = df["Rotational speed [rpm]"] * df["Torque [Nm]"] * 0.10472

    df["Temperature gradient [K]"] = (
        df["Process temperature [K]"] - df["Air temperature [K]"]
    )

    df["Overstrain"] = df["Tool wear [min]"] * df["Torque [Nm]"]

    df["Type"] = df["Type"].map({"L": 0, "M": 1, "H": 2})

    return df[features_order]


def explain_sample(model, sample_df: pd.DataFrame):
    explainer = shap.TreeExplainer(model)

    shap_values = explainer(sample_df)
    sample_shap = shap_values[0, :, 1]

    return sample_shap


if __name__ == "__main__":
    artifact = joblib.load("predictive_maintenance.joblib")
    model = artifact["model"]
    features = artifact["features"]

    danger_telemetry = {
        "Type": "L",
        "Air temperature [K]": 300.2,
        "Process temperature [K]": 309.8,
        "Rotational speed [rpm]": 1210,
        "Torque [Nm]": 68.5,
        "Tool wear [min]": 215,
    }
    sample_df = prepare_input(danger_telemetry, features)
    sample_shap = explain_sample(model, sample_df)

    print(f"Базовая вероятность модели: {sample_shap.base_values:.4f}\n")
    for col, val, impact in zip(
        sample_df.columns, sample_df.iloc[0], sample_shap.values
    ):
        print(f"{col:<25} | Значение: {val:<8.2f} | Вклад SHAP: {impact:+.4f}")

    shap.plots.waterfall(sample_shap, show=False)
    plt.tight_layout()
    plt.show()
