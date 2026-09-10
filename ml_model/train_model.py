import os
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, roc_auc_score
)

def train_and_save_models():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'bank-additional-full_final (3).csv')
    model_dir = os.path.join(base_dir, 'model')
    os.makedirs(model_dir, exist_ok=True)

    print("Loading dataset from:", data_path)
    df = pd.read_csv(data_path)

    # 1. Data Cleaning: Drop Duplicates
    initial_shape = df.shape
    df.drop_duplicates(inplace=True)
    print(f"Dropped duplicates. Shape: {initial_shape} -> {df.shape}")

    # 2. Outlier Handling (IQR) on numeric columns
    outlier_cols = ['age', 'campaign', 'pdays', 'previous', 'cons.conf.idx']
    for col in outlier_cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            LB = Q1 - 1.5 * IQR
            UB = Q3 + 1.5 * IQR
            df = df[(df[col] >= LB) & (df[col] <= UB)]
    print(f"Post outlier handling shape: {df.shape}")

    # Identify features & target
    target_col = 'y'
    df[target_col] = df[target_col].map({'yes': 1, 'no': 0})
    
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Select numerical & categorical features
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'str']).columns.tolist()
    if not categorical_features:
        categorical_features = [col for col in X.columns if col not in numeric_features]

    print("Numeric features:", numeric_features)
    print("Categorical features:", categorical_features)

    # 3. Scikit-Learn Preprocessor (ColumnTransformer)
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, class_weight='balanced', random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=8, class_weight='balanced', random_state=42)
    }

    comparison_results = {}
    best_model_name = "Logistic Regression"
    best_pipeline = None

    for name, clf in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])

        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc = roc_auc_score(y_test, y_prob)

        cm = confusion_matrix(y_test, y_pred).tolist()
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        
        # Sample points for light JSON curve data
        step = max(1, len(fpr) // 50)
        roc_data = {
            "fpr": [round(float(val), 4) for val in fpr[::step]],
            "tpr": [round(float(val), 4) for val in tpr[::step]]
        }

        comparison_results[name] = {
            "algorithm": name,
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "roc_auc": round(float(auc), 4),
            "confusion_matrix": cm,
            "roc_curve": roc_data
        }

        print(f"[{name}] Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}, ROC-AUC: {auc:.4f}")

        if name == "Logistic Regression":
            best_pipeline = pipeline

    # Save primary model pipeline
    pipeline_path = os.path.join(model_dir, 'bankpredict_pipeline.pkl')
    joblib.dump(best_pipeline, pipeline_path)
    print("Saved pipeline model to:", pipeline_path)

    # Save feature names after transformation for XAI
    cat_encoder = best_pipeline.named_steps['preprocessor'].named_transformers_['cat']
    one_hot_cols = list(cat_encoder.get_feature_names_out(categorical_features))
    transformed_feature_names = numeric_features + one_hot_cols

    meta_info = {
        "model_name": "BankPredict AI Primary Model",
        "best_algorithm": best_model_name,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "transformed_feature_names": transformed_feature_names,
        "dataset_rows": int(df.shape[0]),
        "dataset_cols": int(df.shape[1]),
        "models_comparison": comparison_results
    }

    meta_path = os.path.join(model_dir, 'model_comparison.json')
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta_info, f, indent=2)
    print("Saved model comparison metadata to:", meta_path)

if __name__ == "__main__":
    train_and_save_models()
