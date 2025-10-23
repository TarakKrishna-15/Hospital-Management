from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Patient

def home(request):
    return render(request, 'records/login.html')

# ✅ Signup Page
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Create Patient entry automatically
        Patient.objects.create(user=user, age=0, gender="Unknown", medical_condition="N/A")

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')
    return render(request, 'records/signup.html')

# ✅ Login Page
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'records/login.html')

# ✅ Dashboard
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    patient = Patient.objects.get(user=request.user)
    return render(request, 'records/dashboard.html', {'patient': patient, 'site_name': "Digital Health System"})

# ✅ Logout
def logout_view(request):
    logout(request)
    return redirect('login')
