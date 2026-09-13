import logging

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

DB_URI = "postgresql://postgres:mentor@localhost:5432/railway"
TARGET_COLUMN = "Machine failure"
SELECTED_THRESHOLD = 0.15
MODEL_SAVE_PATH = "predictive_maintenance.joblib"

SQL_QUERY = """
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


def load_data(uri: str, query: str) -> pd.DataFrame:
    """Подключение к PostgreSQL и выгрузка сырых данных"""
    logger.info("Подключение к БД")
    engine = create_engine(uri)
    df = pd.read_sql_query(query, engine)
    logger.info(f"Загружено {len(df)} строк.")
    return df


def engineer_features(raw_df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Генерация производных физических признаков")
    df = raw_df.copy()

    # 1. Механическая мощность вала (Вт)
    df["Power [W]"] = df["Rotational speed [rpm]"] * df["Torque [Nm]"] * 0.10472

    # 2. Температурный градиент (способность к теплоотводу)
    df["Temperature gradient [K]"] = (
        df["Process temperature [K]"] - df["Air temperature [K]"]
    )

    # 3. Механическое перенапряжение (износ * крутящий момент)
    df["Overstrain"] = df["Tool wear [min]"] * df["Torque [Nm]"]

    # 4. Порядковое кодирование класса надежности оборудования (L < M < H)
    df["Type"] = df["Type"].map({"L": 0, "M": 1, "H": 2})

    return df


def prepare_data(
    df: pd.DataFrame, target_col: str
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    logger.info("Формирование обучающей и тестовой выборки")
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    return X_train, X_test, y_train, y_test


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """Обучение ансабля с балансировкой весов классов."""
    logger.info("Обучение модели RandomForest")
    model = RandomForestClassifier(
        n_estimators=100, max_depth=10, random_state=42, class_weight="balanced"
    )
    model.fit(X_train, y_train)
    logger.info("Обучение завершено")
    return model


def evalute_tresholds(
    model: RandomForestClassifier,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    tresholds: np.ndarray,
) -> None:
    """Сравнительный анализ влияния порога отсечки на ложные тревоги и пропуски."""
    logger.info("Анализ сетки порогов вероятности:")
    proba = model.predict_proba(X_test)[:, 1]

    print("-" * 55)
    print(f"{'Порог':<10} | {'Пропущено (FN)':<16} | {'Ложные тревоги (FP)':<18}")
    print("-" * 55)

    for t in tresholds:
        preds = (proba >= t).astype(int)
        cm = confusion_matrix(y_test, preds)
        fn = cm[1, 0]
        fp = cm[0, 1]
        print(f"{t:<10.2f} | {fn:<16} | {fp:<18}")
    print("-" * 55)


def save_artifact(
    model: RandomForestClassifier, threshold: float, features: list[str], filepath: str
) -> None:
    """Сериализация модели, порога и списка признаков в один бинарный файл."""
    logger.info(f"Сохранение модели и метаданных в {filepath}...")
    artifact = {"model": model, "threshold": threshold, "features": features}
    joblib.dump(artifact, filepath)
    logger.info("Файл успешно записан на диск.")


def main() -> None:
    """Главная точка входа: связывает все этапы пайплайна воедино."""
    # 1. Загрузка
    raw_df = load_data(DB_URI, SQL_QUERY)

    # 2. Инженерия признаков
    df_engineered = engineer_features(raw_df)

    # 3. Разделение данных
    X_train, X_test, y_train, y_test = prepare_data(df_engineered, TARGET_COLUMN)

    # 4. Обучение
    model = train_model(X_train, y_train)

    # 5. Анализ диапазона порогов
    thresholds_range = np.arange(0.15, 0.36, 0.03)
    evalute_tresholds(model, X_test, y_test, thresholds_range)

    # 6. Финальная оценка на выбранном рабочем пороге
    proba = model.predict_proba(X_test)[:, 1]
    final_preds = (proba >= SELECTED_THRESHOLD).astype(int)
    logger.info(f"Детальный отчет для рабочего порога {SELECTED_THRESHOLD}:")
    print(classification_report(y_test, final_preds))

    # 7. Сохранение артефакта
    feature_names = list(X_train.columns)
    save_artifact(model, SELECTED_THRESHOLD, feature_names, MODEL_SAVE_PATH)


if __name__ == "__main__":
    main()
