import os
import joblib
import pandas as pd
import numpy as np
from .xai import get_explainable_factors

_pipeline = None

def get_pipeline():
    global _pipeline
    if _pipeline is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, 'model', 'bankpredict_pipeline.pkl')
        if os.path.exists(model_path):
            _pipeline = joblib.load(model_path)
        else:
            raise FileNotFoundError(f"Model pipeline not found at {model_path}. Please run train_model.py first.")
    return _pipeline

def sanitize_input(input_dict):
    """Ensure proper data types and default values for missing fields."""
    numeric_cols = {
        'age': 35,
        'campaign': 1,
        'pdays': 999,
        'previous': 0,
        'emp.var.rate': 1.1,
        'cons.price.idx': 93.994,
        'cons.conf.idx': -36.4,
        'euribor3m': 4.857,
        'nr.employed': 5191.0
    }
    
    categorical_cols = {
        'job': 'admin.',
        'marital': 'married',
        'education': 'university.degree',
        'default': 'no',
        'housing': 'yes',
        'loan': 'no',
        'contact': 'cellular',
        'month': 'may',
        'day_of_week': 'mon',
        'poutcome': 'nonexistent'
    }

    clean_data = {}
    for col, default_val in numeric_cols.items():
        val = input_dict.get(col, input_dict.get(col.replace('.', '_'), default_val))
        try:
            clean_data[col] = float(val)
        except (ValueError, TypeError):
            clean_data[col] = float(default_val)

    for col, default_val in categorical_cols.items():
        val = input_dict.get(col, input_dict.get(col.replace('.', '_'), default_val))
        clean_data[col] = str(val).strip().lower() if val else default_val

    return clean_data

def predict_single_customer(input_dict):
    """
    Runs prediction for a single customer input dictionary.
    Returns structured result dictionary.
    """
    clean_data = sanitize_input(input_dict)
    df = pd.DataFrame([clean_data])
    pipeline = get_pipeline()

    prob = float(pipeline.predict_proba(df)[0][1])
    prob_percentage = round(prob * 100, 1)

    is_likely = prob >= 0.5
    prediction_text = "LIKELY TO SUBSCRIBE" if is_likely else "UNLIKELY TO SUBSCRIBE"
    prediction_code = "yes" if is_likely else "no"

    if prob >= 0.75:
        confidence = "High Confidence"
        risk_level = "Low Risk Target"
        recommendation = "High priority customer! Recommend sending tailored term deposit offer and schedule personal call."
    elif prob >= 0.50:
        confidence = "Moderate Confidence"
        risk_level = "Moderate Target"
        recommendation = "Favorable prospect. Contact via primary channel (cellular) with promotional deposit rate."
    elif prob >= 0.25:
        confidence = "Moderate Confidence"
        risk_level = "Unlikely Target"
        recommendation = "Low likelihood. Send automated digital campaign rather than manual agent call."
    else:
        confidence = "High Confidence"
        risk_level = "Low Conversion Target"
        recommendation = "Very low probability of subscription. Do not prioritize for immediate direct sales outreach."

    # Compute Explainable AI factors
    xai_factors = get_explainable_factors(pipeline, df)

    return {
        "prediction": prediction_text,
        "prediction_code": prediction_code,
        "probability": prob_percentage,
        "raw_probability": prob,
        "confidence_level": confidence,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "xai_factors": xai_factors,
        "customer_data": clean_data
    }
