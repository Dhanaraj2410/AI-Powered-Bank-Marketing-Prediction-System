from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Avg, Count

from customers.models import Customer
from predictions.models import Prediction, ModelInformation
from ml_model.predict import predict_single_customer
from .serializers import (
    UserSerializer, PredictionSerializer, ModelInformationSerializer, PredictionInputSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Please provide username, email, and password.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({'message': 'User created successfully', 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful', 'user': UserSerializer(user).data})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def api_predict(request):
    serializer = PredictionInputSerializer(data=request.data)
    if serializer.is_valid():
        input_data = serializer.validated_data
        res = predict_single_customer(input_data)

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

        return Response({
            "id": prediction.id,
            "prediction": res['prediction_code'],
            "prediction_label": res['prediction'],
            "probability": res['probability'],
            "confidence_level": res['confidence_level'],
            "risk_level": res['risk_level'],
            "recommendation": res['recommendation'],
            "xai_factors": res['xai_factors']
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_predictions_list(request):
    if request.user.is_staff:
        queryset = Prediction.objects.all().select_related('customer')
    else:
        queryset = Prediction.objects.filter(user=request.user).select_related('customer')

    serializer = PredictionSerializer(queryset[:100], many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_prediction_detail(request, prediction_id):
    try:
        if request.user.is_staff:
            pred = Prediction.objects.get(id=prediction_id)
        else:
            pred = Prediction.objects.get(id=prediction_id, user=request.user)
        return Response(PredictionSerializer(pred).data)
    except Prediction.DoesNotExist:
        return Response({'error': 'Prediction not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def api_prediction_feedback(request, prediction_id):
    try:
        pred = Prediction.objects.get(id=prediction_id)
        feedback_val = request.data.get('feedback')  # 'yes' or 'no'
        if feedback_val in ['yes', 'no']:
            pred.feedback = feedback_val
            pred.save()
            return Response({'status': 'success', 'feedback': feedback_val})
        return Response({'error': 'Invalid feedback value'}, status=status.HTTP_400_BAD_REQUEST)
    except Prediction.DoesNotExist:
        return Response({'error': 'Prediction not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def api_dashboard_stats(request):
    user_preds = Prediction.objects.filter(user=request.user) if not request.user.is_staff else Prediction.objects.all()

    total_predictions = user_preds.count()
    yes_predictions = user_preds.filter(prediction_result='yes').count()
    no_predictions = user_preds.filter(prediction_result='no').count()
    avg_prob = user_preds.aggregate(Avg('probability'))['probability__avg'] or 0.0

    active_model = ModelInformation.objects.filter(is_active=True).first()
    model_accuracy = active_model.accuracy * 100 if active_model else 77.6

    return Response({
        'total_predictions': total_predictions,
        'yes_predictions': yes_predictions,
        'no_predictions': no_predictions,
        'average_probability': round(avg_prob, 1),
        'active_model_accuracy': round(model_accuracy, 1)
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def api_model_performance(request):
    models_info = ModelInformation.objects.all()
    serializer = ModelInformationSerializer(models_info, many=True)
    return Response(serializer.data)
