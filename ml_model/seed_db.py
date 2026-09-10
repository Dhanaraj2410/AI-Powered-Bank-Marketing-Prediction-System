import os
import sys
import json
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bankpredict.settings')
django.setup()

from predictions.models import ModelInformation
from dataset_manager.models import DatasetInformation

def seed_database():
    meta_path = os.path.join(base_dir, 'model', 'model_comparison.json')

    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        models_comp = data.get("models_comparison", {})
        for name, metrics in models_comp.items():
            obj, created = ModelInformation.objects.get_or_create(
                algorithm=name,
                defaults={
                    "model_name": f"BankPredict AI - {name}",
                    "version": "1.0.0",
                    "accuracy": metrics["accuracy"],
                    "precision": metrics["precision"],
                    "recall": metrics["recall"],
                    "f1_score": metrics["f1_score"],
                    "roc_auc": metrics["roc_auc"],
                    "confusion_matrix_json": metrics["confusion_matrix"],
                    "roc_curve_json": metrics["roc_curve"],
                    "num_features": 19,
                    "is_active": (name == "Logistic Regression")
                }
            )
            if not created:
                obj.accuracy = metrics["accuracy"]
                obj.precision = metrics["precision"]
                obj.recall = metrics["recall"]
                obj.f1_score = metrics["f1_score"]
                obj.roc_auc = metrics["roc_auc"]
                obj.confusion_matrix_json = metrics["confusion_matrix"]
                obj.roc_curve_json = metrics["roc_curve"]
                obj.save()
            print(f"Seeded ModelInformation: {name}")

        DatasetInformation.objects.get_or_create(
            dataset_name="Bank Marketing Direct Marketing Campaign (bank-additional-full)",
            defaults={
                "num_rows": data.get("dataset_rows", 31083),
                "num_columns": data.get("dataset_cols", 20),
                "missing_values": 0,
                "duplicate_rows": 1784
            }
        )
        print("Seeded DatasetInformation successfully.")

if __name__ == "__main__":
    seed_database()
