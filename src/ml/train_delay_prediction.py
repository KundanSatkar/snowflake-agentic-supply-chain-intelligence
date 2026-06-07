import pandas as pd
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)
from sklearn.ensemble import RandomForestClassifier


DATA_PATH = Path("data/processed/clean_candy_sales.csv")
MODEL_OUTPUT_PATH = Path("models/delay_prediction_model.joblib")


def main():

    print("\nLoading dataset...")
    df = pd.read_csv(DATA_PATH)

    print("Dataset Shape:", df.shape)

    print("\nTarget Distribution")
    print(df["IS_DELAYED"].value_counts())

    features = [
        "SHIP_MODE",
        "REGION",
        "DIVISION",
        "PRODUCT_NAME",
        "SALES",
        "UNITS",
        "GROSS_PROFIT",
        "COST",
        "PROFIT_MARGIN",
    ]

    target = "IS_DELAYED"

    X = df[features]
    y = df[target]

    categorical_features = [
        "SHIP_MODE",
        "REGION",
        "DIVISION",
        "PRODUCT_NAME",
    ]

    numeric_features = [
        "SALES",
        "UNITS",
        "GROSS_PROFIT",
        "COST",
        "PROFIT_MARGIN",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features
            ),
            (
                "numeric",
                "passthrough",
                numeric_features
            ),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("\nTraining model...")
    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    print("\n==============================")
    print("DELAY PREDICTION MODEL RESULTS")
    print("==============================")

    print("\nAccuracy:", round(accuracy_score(y_test, predictions), 4))
    print("Precision:", round(precision_score(y_test, predictions, zero_division=0), 4))
    print("Recall:", round(recall_score(y_test, predictions, zero_division=0), 4))
    print("F1 Score:", round(f1_score(y_test, predictions, zero_division=0), 4))

    print("\nClassification Report")
    print(classification_report(y_test, predictions, zero_division=0))

    MODEL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_OUTPUT_PATH)

    print(f"\nModel saved to: {MODEL_OUTPUT_PATH}")


if __name__ == "__main__":
    main()