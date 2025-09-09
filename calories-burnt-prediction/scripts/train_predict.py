#!/usr/bin/env python
import argparse
import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
from xgboost import XGBRegressor


def load_dataset(data_dir: str) -> pd.DataFrame:
    calories_csv = os.path.join(data_dir, 'calories.csv')
    exercise_csv = os.path.join(data_dir, 'exercise.csv')
    if not os.path.exists(calories_csv) or not os.path.exists(exercise_csv):
        print(f"Missing dataset files. Expected: {calories_csv} and {exercise_csv}")
        sys.exit(1)

    calories = pd.read_csv(calories_csv)
    exercise = pd.read_csv(exercise_csv)
    df = pd.concat([exercise, calories['Calories']], axis=1)
    return df


def preprocess(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    df = df.copy()
    # Encode gender values as in the notebook (male->0, female->1)
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].str.lower().map({'male': 0, 'female': 1}).fillna(df['Gender'])
    features = df.drop(columns=['User_ID', 'Calories'], errors='ignore')
    target = df['Calories']
    return features, target


def train_and_evaluate(X: pd.DataFrame, y: pd.Series) -> XGBRegressor:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
    model = XGBRegressor()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mae = metrics.mean_absolute_error(y_test, preds)
    print(f"Mean Absolute Error: {mae:.2f}")
    return model


def predict_example(model: XGBRegressor):
    example = {
        'Gender': 0,  # 0 male, 1 female
        'Age': 25,
        'Height': 175,
        'Weight': 70,
        'Duration': 45,
        'Heart_Rate': 140,
        'Body_Temp': 37.5,
    }
    import pandas as pd
    X = pd.DataFrame([example])
    pred = model.predict(X)[0]
    print(f"Estimated calories burned (example): {pred:.0f} cal")


def main():
    parser = argparse.ArgumentParser(description='Train and predict calories burnt')
    parser.add_argument('--data-dir', default='.', help='Directory containing calories.csv and exercise.csv')
    args = parser.parse_args()

    df = load_dataset(args.data_dir)
    X, y = preprocess(df)
    model = train_and_evaluate(X, y)
    predict_example(model)


if __name__ == '__main__':
    main()


