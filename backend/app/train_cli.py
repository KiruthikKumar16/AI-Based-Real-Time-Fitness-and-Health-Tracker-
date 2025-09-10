import argparse
from pathlib import Path

import joblib
import optuna
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from xgboost import XGBRegressor

from .model_service import MODEL_DIR, MODEL_PATH


def load_xy(data_dir: Path):
    calories = pd.read_csv(data_dir / "calories.csv")
    exercise = pd.read_csv(data_dir / "exercise.csv")
    df = pd.concat([exercise, calories["Calories"]], axis=1)
    df = df.copy()
    if "Gender" in df.columns:
        df["Gender"] = df["Gender"].str.lower().map({"male": 0, "female": 1}).fillna(df["Gender"])
    X = df.drop(columns=["User_ID", "Calories"], errors="ignore")
    y = df["Calories"]
    return X, y


def evaluate_model(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return mean_absolute_error(y_test, preds)


def tune_xgb(X, y):
    def objective(trial: optuna.Trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 100, 600),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        }
        model = XGBRegressor(**params)
        return evaluate_model(model, X, y)

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=20)
    return study.best_params


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="calories-burnt-prediction")
    parser.add_argument("--model-out", default=str(MODEL_PATH))
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    X, y = load_xy(data_dir)

    # Baselines
    models = {
        "linear": LinearRegression(),
        "rf": RandomForestRegressor(n_estimators=300, random_state=2),
        "svr": SVR(C=10.0, epsilon=0.1),
        "xgb": XGBRegressor(),
    }
    scores = {name: evaluate_model(m, X, y) for name, m in models.items()}
    best_name = min(scores, key=scores.get)
    print("MAE:", scores)

    # Tune XGB
    best_params = tune_xgb(X, y)
    tuned = XGBRegressor(**best_params)
    tuned_mae = evaluate_model(tuned, X, y)
    print("tuned_xgb_mae:", tuned_mae)

    best_model = tuned if tuned_mae < scores[best_name] else models[best_name]
    print("selected:", "tuned_xgb" if best_model is tuned else best_name)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model.fit(X, y), args.model_out)
    print("saved:", args.model_out)


if __name__ == "__main__":
    main()


