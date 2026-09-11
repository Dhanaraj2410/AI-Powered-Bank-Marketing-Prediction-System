from django.core.management.base import BaseCommand
import subprocess
import sys
import os

class Command(BaseCommand):
    help = 'Retrains the Scikit-learn Logistic Regression pipeline and updates model metadata in database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Logistic Regression Model Retraining..."))
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        train_script = os.path.join(base_dir, 'ml_model', 'train_model.py')
        
        if not os.path.exists(train_script):
            self.stderr.write(f"Training script not found at {train_script}")
            return

        result = subprocess.run([sys.executable, train_script], capture_output=True, text=True)
        
        if result.returncode == 0:
            self.stdout.write(self.style.SUCCESS("Model training finished successfully."))
            self.stdout.write(result.stdout)
        else:
            self.stderr.write(self.style.ERROR(f"Model training failed: {result.stderr}"))
