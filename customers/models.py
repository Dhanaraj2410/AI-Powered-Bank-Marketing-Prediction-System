from django.db import models

class Customer(models.Model):
    age = models.IntegerField()
    job = models.CharField(max_length=50)
    marital = models.CharField(max_length=30)
    education = models.CharField(max_length=50)
    default_credit = models.CharField(max_length=20, default='no')
    housing_loan = models.CharField(max_length=20, default='yes')
    personal_loan = models.CharField(max_length=20, default='no')
    contact_type = models.CharField(max_length=30, default='cellular')
    month = models.CharField(max_length=20, default='may')
    day_of_week = models.CharField(max_length=20, default='mon')
    campaign = models.IntegerField(default=1)
    pdays = models.IntegerField(default=999)
    previous = models.IntegerField(default=0)
    poutcome = models.CharField(max_length=30, default='nonexistent')
    emp_var_rate = models.FloatField(default=1.1)
    cons_price_idx = models.FloatField(default=93.994)
    cons_conf_idx = models.FloatField(default=-36.4)
    euribor3m = models.FloatField(default=4.857)
    nr_employed = models.FloatField(default=5191.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Customer #{self.id} ({self.job}, {self.age}yo)"
