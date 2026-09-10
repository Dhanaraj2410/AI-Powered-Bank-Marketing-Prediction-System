from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from predictions.models import ModelInformation, Prediction

def home_view(request):
    active_model = ModelInformation.objects.filter(is_active=True).first()
    model_accuracy = round(active_model.accuracy * 100, 1) if active_model else 77.6
    total_predictions = Prediction.objects.count()
    successful_predictions = Prediction.objects.filter(prediction_result='yes').count()
    active_users = User.objects.count()

    context = {
        'model_accuracy': model_accuracy,
        'total_predictions': total_predictions,
        'successful_predictions': successful_predictions,
        'active_users': active_users,
    }
    return render(request, 'home.html', context)

def about_view(request):
    return render(request, 'about.html')

def how_it_works_view(request):
    return render(request, 'how_it_works.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        messages.success(request, f"Thank you, {name}! Your message has been received. Our team will reach out shortly.")
        return redirect('contact')
    return render(request, 'contact.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone', '')
        occupation = request.POST.get('occupation', '')

        if not username or not email or not password:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'accounts/register.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, phone=phone, occupation=occupation)
        login(request, user)
        messages.success(request, f"Welcome to BankPredict AI, {user.username}!")
        return redirect('dashboard')

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()

            profile.phone = request.POST.get('phone', '')
            profile.occupation = request.POST.get('occupation', '')
            profile.bio = request.POST.get('bio', '')
            profile.save()
            messages.success(request, "Profile updated successfully.")

        elif action == 'change_password':
            old_pass = request.POST.get('old_password')
            new_pass = request.POST.get('new_password')
            confirm_pass = request.POST.get('confirm_password')

            if not request.user.check_password(old_pass):
                messages.error(request, "Current password is incorrect.")
            elif new_pass != confirm_pass:
                messages.error(request, "New passwords do not match.")
            elif len(new_pass) < 6:
                messages.error(request, "Password must be at least 6 characters.")
            else:
                request.user.set_password(new_pass)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully.")

        return redirect('profile')

    user_predictions_count = Prediction.objects.filter(user=request.user).count()
    context = {
        'profile': profile,
        'user_predictions_count': user_predictions_count
    }
    return render(request, 'accounts/profile.html', context)
