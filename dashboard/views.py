from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from predictions.models import Prediction, ModelInformation, BatchPrediction
from dataset_manager.models import DatasetInformation
from customers.models import Customer

@login_required
def dashboard_view(request):
    user_preds = Prediction.objects.filter(user=request.user) if not request.user.is_staff else Prediction.objects.all()

    total_predictions = user_preds.count()
    yes_predictions = user_preds.filter(prediction_result='yes').count()
    no_predictions = user_preds.filter(prediction_result='no').count()
    
    avg_prob_val = user_preds.aggregate(Avg('probability'))['probability__avg']
    avg_probability = round(avg_prob_val, 1) if avg_prob_val is not None else 0.0

    active_model = ModelInformation.objects.filter(is_active=True).first()
    model_accuracy = round(active_model.accuracy * 100, 1) if active_model else 77.6

    # Chart 1: Yes vs No Predictions
    yes_vs_no = [yes_predictions, no_predictions]

    # Chart 2: Predictions by Month (from Customer)
    month_counts = user_preds.values('customer__month').annotate(total=Count('id')).order_by('-total')[:6]
    month_labels = [m['customer__month'].capitalize() for m in month_counts]
    month_data = [m['total'] for m in month_counts]

    # Chart 3: Probability Distribution Ranges (<25%, 25-50%, 50-75%, >75%)
    prob_ranges = [
        user_preds.filter(probability__lt=25).count(),
        user_preds.filter(probability__gte=25, probability__lt=50).count(),
        user_preds.filter(probability__gte=50, probability__lt=75).count(),
        user_preds.filter(probability__gte=75).count(),
    ]

    # Chart 4: Predictions by Job
    job_counts = user_preds.values('customer__job').annotate(total=Count('id')).order_by('-total')[:5]
    job_labels = [j['customer__job'].title() for j in job_counts]
    job_data = [j['total'] for j in job_counts]

    # Chart 5: Predictions by Contact Type
    contact_counts = user_preds.values('customer__contact_type').annotate(total=Count('id'))
    contact_labels = [c['customer__contact_type'].title() for c in contact_counts]
    contact_data = [c['total'] for c in contact_counts]

    recent_predictions = user_preds.select_related('customer')[:5]

    context = {
        'total_predictions': total_predictions,
        'yes_predictions': yes_predictions,
        'no_predictions': no_predictions,
        'avg_probability': avg_probability,
        'model_accuracy': model_accuracy,
        'yes_vs_no': yes_vs_no,
        'month_labels': month_labels,
        'month_data': month_data,
        'prob_ranges': prob_ranges,
        'job_labels': job_labels,
        'job_data': job_data,
        'contact_labels': contact_labels,
        'contact_data': contact_data,
        'recent_predictions': recent_predictions,
        'active_model': active_model,
    }
    return render(request, 'dashboard/user_dashboard.html', context)

@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    total_users = User.objects.count()
    total_predictions = Prediction.objects.count()
    yes_predictions = Prediction.objects.filter(prediction_result='yes').count()
    no_predictions = Prediction.objects.filter(prediction_result='no').count()
    total_customers = Customer.objects.count()
    total_batches = BatchPrediction.objects.count()

    datasets = DatasetInformation.objects.all().order_by('-upload_date')
    models_list = ModelInformation.objects.all()
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    recent_predictions = Prediction.objects.all().select_related('user', 'customer')[:5]

    context = {
        'total_users': total_users,
        'total_predictions': total_predictions,
        'yes_predictions': yes_predictions,
        'no_predictions': no_predictions,
        'total_customers': total_customers,
        'total_batches': total_batches,
        'datasets': datasets,
        'models_list': models_list,
        'recent_users': recent_users,
        'recent_predictions': recent_predictions,
    }
    return render(request, 'admin_custom/dashboard.html', context)
