from pathlib import Path
from typing import Optional

import joblib
import pandas as pd
from xgboost import XGBRegressor


MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_PATH = MODEL_DIR / "calories_xgb.joblib"


def ensure_model(data_dir: Optional[Path] = None) -> XGBRegressor:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)

    # Fallback: train a quick model if datasets are available
    if data_dir is None:
        raise FileNotFoundError("Model not found and no data_dir provided to train.")

    calories = pd.read_csv(data_dir / "calories.csv")
    exercise = pd.read_csv(data_dir / "exercise.csv")
    df = pd.concat([exercise, calories["Calories"]], axis=1)
    df = df.copy()
    if "Gender" in df.columns:
        df["Gender"] = df["Gender"].str.lower().map({"male": 0, "female": 1}).fillna(df["Gender"])
    X = df.drop(columns=["User_ID", "Calories"], errors="ignore")
    y = df["Calories"]

    model = XGBRegressor()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model


