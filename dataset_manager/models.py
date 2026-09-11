from django.db import models
from django.contrib.auth.models import User

# Comment 11: DatasetInformation tracks metadata of uploaded CSV datasets, row counts, missing values, and uploaders.
class DatasetInformation(models.Model):
    dataset_name = models.CharField(max_length=255)
    num_rows = models.IntegerField()
    num_columns = models.IntegerField()
    missing_values = models.IntegerField(default=0)
    duplicate_rows = models.IntegerField(default=0)
    file_path = models.CharField(max_length=500, blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    # Comment 12: Returns dataset summary string with dimensions for dashboard UI displays.
    def __str__(self):
        return f"{self.dataset_name} ({self.num_rows} rows x {self.num_columns} cols)"
