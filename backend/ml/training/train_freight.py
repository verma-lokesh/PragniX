from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from xgboost import XGBRegressor


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data" / "processed" / "freight_training.csv"

ARTIFACT_DIR = BASE_DIR / "ml" / "artifacts"

ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


TARGET_7D = "target_freight_rate_7d"
TARGET_30D = "target_freight_rate_30d"


def load_dataset():

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    if "date" not in df.columns:
        raise ValueError("Dataset must contain a 'date' column.")

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date").reset_index(drop=True)

    required_targets = [TARGET_7D, TARGET_30D]

    for target in required_targets:

        if target not in df.columns:
            raise ValueError(f"Missing target column: {target}")

    return df


def split_dataset(df):

    train_end = pd.Timestamp("2024-05-18")

    validation_end = pd.Timestamp("2025-06-28")

    train_df = df[df["date"] <= train_end].copy()

    validation_df = df[(df["date"] > train_end) & (df["date"] <= validation_end)].copy()

    test_df = df[df["date"] > validation_end].copy()

    print("\nDataset split")
    print("-" * 50)

    print(f"Train      : {len(train_df):,}")

    print(f"Validation : {len(validation_df):,}")

    print(f"Test       : {len(test_df):,}")

    return (train_df, validation_df, test_df)


def create_preprocessor(df):

    excluded = ["date", TARGET_7D, TARGET_30D]

    feature_columns = [column for column in df.columns if column not in excluded]

    X = df[feature_columns]

    categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

    numerical_features = [
        column for column in feature_columns if column not in categorical_features
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_features,
            ),
            ("numerical", "passthrough", numerical_features),
        ]
    )

    return (preprocessor, feature_columns, categorical_features, numerical_features)


def create_model():

    return XGBRegressor(
        n_estimators=500,
        max_depth=7,
        learning_rate=0.04,
        min_child_weight=3,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_alpha=0.05,
        reg_lambda=1.0,
        objective="reg:squarederror",
        eval_metric="mae",
        random_state=42,
        n_jobs=-1,
        tree_method="hist",
    )


def calculate_metrics(actual, predicted):

    mae = mean_absolute_error(actual, predicted)

    rmse = np.sqrt(mean_squared_error(actual, predicted))

    r2 = r2_score(actual, predicted)

    mape = (
        np.mean(np.abs((actual - predicted) / np.maximum(np.abs(actual), 1e-8))) * 100
    )

    return {
        "MAE": round(float(mae), 4),
        "RMSE": round(float(rmse), 4),
        "R2": round(float(r2), 4),
        "MAPE_percent": round(float(mape), 4),
    }


def train_model(
    name, target, train_df, validation_df, test_df, preprocessor, feature_columns
):

    print("\n")
    print("=" * 70)
    print(f"Training {name}")
    print("=" * 70)

    X_train_raw = train_df[feature_columns]

    X_validation_raw = validation_df[feature_columns]

    X_test_raw = test_df[feature_columns]

    y_train = train_df[target]

    y_validation = validation_df[target]

    y_test = test_df[target]

    print(f"Training rows: {len(X_train_raw):,}")

    X_train = preprocessor.fit_transform(X_train_raw)

    X_validation = preprocessor.transform(X_validation_raw)

    X_test = preprocessor.transform(X_test_raw)

    print(f"Encoded features: {X_train.shape[1]:,}")

    model = create_model()

    model.fit(X_train, y_train, eval_set=[(X_validation, y_validation)], verbose=False)

    validation_prediction = model.predict(X_validation)

    test_prediction = model.predict(X_test)

    validation_metrics = calculate_metrics(y_validation, validation_prediction)

    test_metrics = calculate_metrics(y_test, test_prediction)

    print("\nValidation metrics")

    for key, value in validation_metrics.items():
        print(f"{key}: {value}")

    print("\nTest metrics")

    for key, value in test_metrics.items():
        print(f"{key}: {value}")

    model_path = ARTIFACT_DIR / f"{name}.joblib"

    joblib.dump(model, model_path)

    print(f"\nModel saved: {model_path}")

    return {
        "model": model,
        "validation_metrics": validation_metrics,
        "test_metrics": test_metrics,
    }


def save_feature_importance(model, preprocessor):

    try:

        feature_names = preprocessor.get_feature_names_out()

        importance = model.feature_importances_

        importance_df = pd.DataFrame(
            {"feature": feature_names, "importance": importance}
        )

        importance_df = importance_df.sort_values(
            "importance", ascending=False
        ).reset_index(drop=True)

        path = ARTIFACT_DIR / "freight_feature_importance.csv"

        importance_df.to_csv(path, index=False)

        print(f"Feature importance saved: {path}")

    except Exception as error:

        print(f"Feature importance error: {error}")


def main():

    print("\nAnchorIQ Freight Forecasting Training")

    print("=" * 70)

    df = load_dataset()

    print(f"Dataset rows: {len(df):,}")

    print(f"Dataset columns: {len(df.columns)}")

    (train_df, validation_df, test_df) = split_dataset(df)

    (preprocessor, feature_columns, categorical_features, numerical_features) = (
        create_preprocessor(df)
    )

    print(f"\nCategorical features: " f"{len(categorical_features)}")

    print(f"Numerical features: " f"{len(numerical_features)}")

    model_7d = train_model(
        name="freight_xgb_7d",
        target=TARGET_7D,
        train_df=train_df,
        validation_df=validation_df,
        test_df=test_df,
        preprocessor=preprocessor,
        feature_columns=feature_columns,
    )

    model_30d = train_model(
        name="freight_xgb_30d",
        target=TARGET_30D,
        train_df=train_df,
        validation_df=validation_df,
        test_df=test_df,
        preprocessor=preprocessor,
        feature_columns=feature_columns,
    )

    preprocessor_path = ARTIFACT_DIR / "freight_preprocessor.joblib"

    joblib.dump(preprocessor, preprocessor_path)

    save_feature_importance(model_7d["model"], preprocessor)

    metadata = {
        "model_type": "XGBoost",
        "dataset_rows": len(df),
        "feature_count": len(feature_columns),
        "encoded_feature_count": model_7d["model"].n_features_in_,
        "train_rows": len(train_df),
        "validation_rows": len(validation_df),
        "test_rows": len(test_df),
        "categorical_features": categorical_features,
        "numerical_features": numerical_features,
        "models": {
            "freight_7d": model_7d["test_metrics"],
            "freight_30d": model_30d["test_metrics"],
        },
        "split": {"train_end": "2024-05-18", "validation_end": "2025-06-28"},
        "data_status": "synthetic development data",
    }

    metadata_path = ARTIFACT_DIR / "training_metadata.json"

    with open(metadata_path, "w") as file:

        json.dump(metadata, file, indent=4)

    print("\n")
    print("=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)

    print(f"\nArtifacts directory:" f"\n{ARTIFACT_DIR}")


if __name__ == "__main__":
    main()
