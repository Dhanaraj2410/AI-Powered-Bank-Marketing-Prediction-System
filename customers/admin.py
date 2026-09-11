from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'age', 'marital', 'education', 'housing_loan', 'personal_loan', 'created_at')
    list_filter = ('job', 'marital', 'education', 'housing_loan', 'personal_loan')
    search_fields = ('job', 'education')
