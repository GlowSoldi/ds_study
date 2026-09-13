import logging

import joblib
import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MaintenancePredictor:
    REQUIRED_FIELDS: tuple[str, ...] = (
        "Type",
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]",
    )

    def __init__(self, artifact_path: str = "predictive_maintenance.joblib") -> None:
        """Загрузка артефакта модели и конфига из файла"""
        logger.info(f"Загрузка артефакта из {artifact_path}")
        artifact = joblib.load(artifact_path)

        self.model = artifact["model"]
        self.threshold = artifact["threshold"]
        self.features = artifact["features"]
        logger.info("Модель успешно загружена и готова к работе")

    def _validate_input(self, raw_data: dict) -> None:
        """Проверка наличия всех обязательных показателей"""
        missing = [field for field in self.REQUIRED_FIELDS if field not in raw_data]
        if missing:
            raise ValueError(f"Отсутствуют обязательные параметры: {missing}")

    def _engineer_features(self, raw_data: dict) -> pd.DataFrame:
        """Расчет производных физ. параметров для одного измерения."""
        df = pd.DataFrame([raw_data])

        df["Power [W]"] = df["Rotational speed [rpm]"] * df["Torque [Nm]"] * 0.10472

        df["Temperature gradient [K]"] = (
            df["Process temperature [K]"] - df["Air temperature [K]"]
        )

        df["Overstrain"] = df["Tool wear [min]"] * df["Torque [Nm]"]

        df["Type"] = df["Type"].map({"L": 0, "M": 1, "H": 2})

        return df[self.features]

    def predict(self, raw_data: dict) -> dict:
        """Полный цикл предиктивной диагностики узла"""
        self._validate_input(raw_data)
        features_df = self._engineer_features(raw_data)

        prob_failure = float(self.model.predict_proba(features_df)[0, 1])
        is_alarm = prob_failure >= self.threshold

        return {
            "alarm": is_alarm,
            "risk_score": round(prob_failure * 100, 2),
            "status": "ТРЕВОГА: РИСК АВАРИИ" if is_alarm else "Штатный режим",
        }


if __name__ == "__main__":
    predictor = MaintenancePredictor()

    healthy_telemetry = {
        "Type": "M",
        "Air temperature [K]": 298.1,
        "Process temperature [K]": 308.6,
        "Rotational speed [rpm]": 1551,
        "Torque [Nm]": 42.8,
        "Tool wear [min]": 15,
    }
    print("\nРезультат диагностики №1 (Штатный):")
    print(predictor.predict(healthy_telemetry))

    danger_telemetry = {
        "Type": "L",
        "Air temperature [K]": 300.2,
        "Process temperature [K]": 309.8,
        "Rotational speed [rpm]": 1210,
        "Torque [Nm]": 68.5,
        "Tool wear [min]": 215,
    }
    print("\nРезультат диагностики №2 (Критический):")
    print(predictor.predict(danger_telemetry))
