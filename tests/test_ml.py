from django.test import TestCase
from ml_model.predict import predict_single_customer, get_pipeline

class MLModelTests(TestCase):
    def test_pipeline_loading(self):
        pipeline = get_pipeline()
        self.assertIsNotNone(pipeline)

    def test_predict_single_customer(self):
        sample_input = {
            'age': 40,
            'job': 'technician',
            'marital': 'married',
            'education': 'university.degree',
            'default': 'no',
            'housing': 'yes',
            'loan': 'no',
            'contact': 'cellular',
            'month': 'may',
            'day_of_week': 'mon',
            'campaign': 2,
            'previous': 0,
            'poutcome': 'nonexistent',
            'emp.var.rate': 1.1,
            'cons.price.idx': 93.994,
            'cons.conf.idx': -36.4,
            'euribor3m': 4.857,
            'nr.employed': 5191.0
        }
        
        result = predict_single_customer(sample_input)
        self.assertIn('prediction', result)
        self.assertIn(result['prediction_code'], ['yes', 'no'])
        self.assertTrue(0.0 <= result['probability'] <= 100.0)
        self.assertIn('xai_factors', result)
        self.assertIn('positive', result['xai_factors'])
        self.assertIn('negative', result['xai_factors'])
