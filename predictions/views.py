import csv
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from customers.models import Customer
from .models import Prediction, BatchPrediction, ModelInformation
from ml_model.predict import predict_single_customer, get_pipeline
from ml_model.xai import get_explainable_factors

@login_required
def predict_view(request):
    if request.method == 'POST':
        try:
            input_dict = {
                'age': request.POST.get('age', 35),
                'job': request.POST.get('job', 'admin.'),
                'marital': request.POST.get('marital', 'married'),
                'education': request.POST.get('education', 'university.degree'),
                'default': request.POST.get('default', 'no'),
                'housing': request.POST.get('housing', 'yes'),
                'loan': request.POST.get('loan', 'no'),
                'contact': request.POST.get('contact', 'cellular'),
                'month': request.POST.get('month', 'may'),
                'day_of_week': request.POST.get('day_of_week', 'mon'),
                'campaign': request.POST.get('campaign', 1),
                'pdays': request.POST.get('pdays', 999),
                'previous': request.POST.get('previous', 0),
                'poutcome': request.POST.get('poutcome', 'nonexistent'),
                'emp.var.rate': request.POST.get('emp_var_rate', 1.1),
                'cons.price.idx': request.POST.get('cons_price_idx', 93.994),
                'cons.conf.idx': request.POST.get('cons_conf_idx', -36.4),
                'euribor3m': request.POST.get('euribor3m', 4.857),
                'nr.employed': request.POST.get('nr_employed', 5191.0),
            }

            res = predict_single_customer(input_dict)

            # Create Customer record in MySQL
            c_data = res['customer_data']
            customer = Customer.objects.create(
                age=int(c_data['age']),
                job=c_data['job'],
                marital=c_data['marital'],
                education=c_data['education'],
                default_credit=c_data['default'],
                housing_loan=c_data['housing'],
                personal_loan=c_data['loan'],
                contact_type=c_data['contact'],
                month=c_data['month'],
                day_of_week=c_data['day_of_week'],
                campaign=int(c_data['campaign']),
                pdays=int(c_data['pdays']),
                previous=int(c_data['previous']),
                poutcome=c_data['poutcome'],
                emp_var_rate=c_data['emp.var.rate'],
                cons_price_idx=c_data['cons.price.idx'],
                cons_conf_idx=c_data['cons.conf.idx'],
                euribor3m=c_data['euribor3m'],
                nr_employed=c_data['nr.employed']
            )

            # Create Prediction record
            prediction = Prediction.objects.create(
                user=request.user,
                customer=customer,
                prediction_result=res['prediction_code'],
                probability=res['probability'],
                confidence_level=res['confidence_level'],
                risk_level=res['risk_level'],
                recommendation=res['recommendation'],
                xai_factors_json=res['xai_factors']
            )

            return redirect('prediction_result', prediction_id=prediction.id)

        except Exception as e:
            messages.error(request, f"Error processing prediction: {str(e)}")
            return render(request, 'predictions/predict.html')

    return render(request, 'predictions/predict.html')

@login_required
def prediction_result_view(request, prediction_id):
    prediction = get_object_or_404(Prediction, id=prediction_id)
    if not request.user.is_staff and prediction.user != request.user:
        messages.error(request, "Unauthorized access to prediction result.")
        return redirect('history')

    active_model = ModelInformation.objects.filter(is_active=True).first()
    model_name = active_model.algorithm if active_model else "Logistic Regression"

    context = {
        'prediction': prediction,
        'customer': prediction.customer,
        'model_name': model_name,
        'xai_factors': prediction.xai_factors_json
    }
    return render(request, 'predictions/result.html', context)

@login_required
def batch_predict_view(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please upload a valid CSV file.")
            return render(request, 'predictions/batch_predict.html')

        try:
            df = pd.read_csv(csv_file)
            total_records = len(df)
            if total_records == 0:
                messages.error(request, "The uploaded CSV file is empty.")
                return render(request, 'predictions/batch_predict.html')

            pipeline = get_pipeline()
            predictions_list = []
            yes_count = 0
            no_count = 0
            prob_sum = 0.0

            for index, row in df.iterrows():
                row_dict = row.to_dict()
                res = predict_single_customer(row_dict)

                c_data = res['customer_data']
                customer = Customer.objects.create(
                    age=int(c_data['age']),
                    job=c_data['job'],
                    marital=c_data['marital'],
                    education=c_data['education'],
                    default_credit=c_data['default'],
                    housing_loan=c_data['housing'],
                    personal_loan=c_data['loan'],
                    contact_type=c_data['contact'],
                    month=c_data['month'],
                    day_of_week=c_data['day_of_week'],
                    campaign=int(c_data['campaign']),
                    pdays=int(c_data['pdays']),
                    previous=int(c_data['previous']),
                    poutcome=c_data['poutcome'],
                    emp_var_rate=c_data['emp.var.rate'],
                    cons_price_idx=c_data['cons.price.idx'],
                    cons_conf_idx=c_data['cons.conf.idx'],
                    euribor3m=c_data['euribor3m'],
                    nr_employed=c_data['nr.employed']
                )

                pred_obj = Prediction.objects.create(
                    user=request.user,
                    customer=customer,
                    prediction_result=res['prediction_code'],
                    probability=res['probability'],
                    confidence_level=res['confidence_level'],
                    risk_level=res['risk_level'],
                    recommendation=res['recommendation'],
                    xai_factors_json=res['xai_factors']
                )
                predictions_list.append(pred_obj)

                if res['prediction_code'] == 'yes':
                    yes_count += 1
                else:
                    no_count += 1
                prob_sum += res['probability']

            avg_prob = round(prob_sum / total_records, 1) if total_records > 0 else 0.0

            batch_obj = BatchPrediction.objects.create(
                user=request.user,
                file_name=csv_file.name,
                total_records=total_records,
                yes_count=yes_count,
                no_count=no_count,
                avg_probability=avg_prob
            )

            messages.success(request, f"Successfully processed batch CSV! {total_records} customer predictions generated.")
            context = {
                'batch': batch_obj,
                'predictions': predictions_list[:50],  # show first 50 rows in table
                'total_count': total_records
            }
            return render(request, 'predictions/batch_predict.html', context)

        except Exception as e:
            messages.error(request, f"Error parsing CSV file: {str(e)}")
            return render(request, 'predictions/batch_predict.html')

    return render(request, 'predictions/batch_predict.html')

@login_required
def download_batch_csv_view(request, batch_id):
    batch = get_object_or_404(BatchPrediction, id=batch_id)
    if not request.user.is_staff and batch.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="predictions_batch_{batch.id}.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Prediction ID', 'Age', 'Job', 'Marital', 'Education', 'Housing Loan',
        'Personal Loan', 'Contact Type', 'Month', 'Campaign',
        'Prediction Result', 'Probability (%)', 'Confidence Level', 'Created Date'
    ])

    user_preds = Prediction.objects.filter(user=batch.user).order_by('-created_at')[:batch.total_records]
    for p in user_preds:
        c = p.customer
        writer.writerow([
            p.id, c.age, c.job, c.marital, c.education, c.housing_loan,
            c.personal_loan, c.contact_type, c.month, c.campaign,
            p.prediction_result.upper(), p.probability, p.confidence_level,
            p.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response

@login_required
def history_view(request):
    if request.user.is_staff:
        predictions_qs = Prediction.objects.all().select_related('user', 'customer')
    else:
        predictions_qs = Prediction.objects.filter(user=request.user).select_related('customer')

    # Search & Filters
    search_query = request.GET.get('search', '').strip()
    result_filter = request.GET.get('result', '').strip()
    job_filter = request.GET.get('job', '').strip()
    sort_order = request.GET.get('sort', '-created_at')

    if search_query:
        predictions_qs = predictions_qs.filter(
            Q(customer__job__icontains=search_query) |
            Q(customer__education__icontains=search_query) |
            Q(customer__contact_type__icontains=search_query)
        )

    if result_filter:
        predictions_qs = predictions_qs.filter(prediction_result=result_filter.lower())

    if job_filter:
        predictions_qs = predictions_qs.filter(customer__job=job_filter)

    if sort_order in ['created_at', '-created_at', 'probability', '-probability']:
        predictions_qs = predictions_qs.order_by(sort_order)

    paginator = Paginator(predictions_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'result_filter': result_filter,
        'job_filter': job_filter,
        'sort_order': sort_order,
    }
    return render(request, 'predictions/history.html', context)

@login_required
def export_history_csv_view(request):
    if request.user.is_staff:
        predictions_qs = Prediction.objects.all().select_related('user', 'customer')
    else:
        predictions_qs = Prediction.objects.filter(user=request.user).select_related('customer')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="prediction_history.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Prediction ID', 'User', 'Age', 'Job', 'Marital', 'Education', 'Default',
        'Housing Loan', 'Personal Loan', 'Contact Type', 'Month', 'Day of Week',
        'Campaign', 'Prediction Result', 'Probability (%)', 'Confidence', 'Date'
    ])

    for p in predictions_qs:
        c = p.customer
        username = p.user.username if p.user else 'Anonymous'
        writer.writerow([
            p.id, username, c.age, c.job, c.marital, c.education, c.default_credit,
            c.housing_loan, c.personal_loan, c.contact_type, c.month, c.day_of_week,
            c.campaign, p.prediction_result.upper(), p.probability, p.confidence_level,
            p.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response

@login_required
def prediction_detail_view(request, prediction_id):
    prediction = get_object_or_404(Prediction, id=prediction_id)
    if not request.user.is_staff and prediction.user != request.user:
        messages.error(request, "Unauthorized access to prediction detail.")
        return redirect('history')

    context = {
        'prediction': prediction,
        'customer': prediction.customer,
        'xai_factors': prediction.xai_factors_json
    }
    return render(request, 'predictions/detail.html', context)

def model_performance_view(request):
    models_info = ModelInformation.objects.all()
    active_model = ModelInformation.objects.filter(is_active=True).first()

    context = {
        'models_info': models_info,
        'active_model': active_model,
    }
    return render(request, 'model_performance.html', context)
