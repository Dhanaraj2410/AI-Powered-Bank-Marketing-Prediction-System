import os
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DatasetInformation

@login_required
def dataset_list_view(request):
    if not request.user.is_staff:
        messages.error(request, "Admin privileges required.")
        return redirect('dashboard')

    datasets = DatasetInformation.objects.all().order_by('-upload_date')
    return render(request, 'admin_custom/dataset_list.html', {'datasets': datasets})

@login_required
def upload_dataset_view(request):
    if not request.user.is_staff:
        messages.error(request, "Admin privileges required.")
        return redirect('dashboard')

    if request.method == 'POST' and request.FILES.get('dataset_file'):
        csv_file = request.FILES['dataset_file']
        dataset_name = request.POST.get('dataset_name', csv_file.name)

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please upload a valid CSV file.")
            return redirect('dataset_list')

        try:
            df = pd.read_csv(csv_file)
            num_rows, num_cols = df.shape
            missing_val = int(df.isnull().sum().sum())
            dup_val = int(df.duplicated().sum())

            DatasetInformation.objects.create(
                dataset_name=dataset_name,
                num_rows=num_rows,
                num_columns=num_cols,
                missing_values=missing_val,
                duplicate_rows=dup_val,
                file_path=csv_file.name,
                uploaded_by=request.user
            )

            messages.success(
                request,
                f"Dataset '{dataset_name}' validated and uploaded! "
                f"Rows: {num_rows}, Columns: {num_cols}, Missing: {missing_val}, Duplicates: {dup_val}"
            )
            return redirect('dataset_list')

        except Exception as e:
            messages.error(request, f"Failed to parse dataset CSV: {str(e)}")
            return redirect('dataset_list')

    return redirect('dataset_list')
